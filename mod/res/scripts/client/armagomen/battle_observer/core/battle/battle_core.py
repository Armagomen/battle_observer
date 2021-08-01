from CurrentVehicle import g_currentVehicle
from DogTagComponent import DogTagComponent
from PlayerEvents import g_playerEvents
from VehicleGunRotator import VehicleGunRotator
from armagomen.constants import MAIN, GLOBAL, DAMAGE_LOG
from armagomen.utils.common import setMaxFrameRate, overrideMethod, logInfo, getPlayer
from armagomen.utils.events import g_events
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.controllers import msgs_ctrl
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl

BASE_NOTIFICATIONS = (msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND)


class BattleCore(object):

    def __init__(self, settings):
        self.settings = settings
        g_playerEvents.onArenaCreated += self.onArenaCreated
        settings.onModSettingsChanged += self.onModSettingsChanged
        overrideMethod(_ClientArenaVisitor, "hasDogTag")(self.hasDogTag)
        overrideMethod(DogTagComponent, "_isObserving")(self._isObservingDogTagFix)
        overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByTankmen")(self.setSoundMode)
        overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByCommanderSkinID")(self.setSoundMode)

    def setSoundMode(self, base, *args, **kwargs):
        if self.settings.main[MAIN.IGNORE_COMMANDERS]:
            return False
        return base(*args, **kwargs)

    def hasDogTag(self, base, *args, **kwargs):
        return False if self.settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)

    @staticmethod
    def _isObservingDogTagFix(*args):
        player = getPlayer()
        if player is None or player.vehicle is None:
            return True
        else:
            return not player.vehicle.isPlayerVehicle

    @staticmethod
    def onModSettingsChanged(settings, blockID):
        if blockID == MAIN.NAME:
            if settings[MAIN.ENABLE_FPS_LIMITER]:
                setMaxFrameRate(settings[MAIN.MAX_FRAME_RATE])
            if settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
                msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
            elif not settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
                msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND = BASE_NOTIFICATIONS

    @staticmethod
    @overrideMethod(VehicleGunRotator, "__updateGunMarker")
    def updateRotationAndGunMarker(base, rotator, *args, **kwargs):
        base(rotator, *args, **kwargs)
        g_events.onDispersionAngleChanged(rotator)

    def onArenaCreated(self):
        if self.settings.log_total[GLOBAL.ENABLED]:
            try:
                dossier = g_currentVehicle.getDossier()
                if dossier:
                    damage = dossier.getRandomStats().getAvgDamage()
                    assist = dossier.getRandomStats().getDamageAssistedEfficiencyWithStan()
                    if damage is not None:
                        damage = round(damage)
                        DAMAGE_LOG.AVG_DAMAGE_DATA = damage
                        logInfo("set vehicle efficiency (avgDamage: {}, avgAssist: {})".format(damage, assist))
            except AttributeError:
                DAMAGE_LOG.AVG_DAMAGE_DATA = GLOBAL.ZERO
