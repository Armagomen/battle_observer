from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from SoundGroups import SoundModes
from armagomen.battle_observer.core.bo_constants import MAIN, SOUND_MODES, GLOBAL, DAMAGE_LOG
from armagomen.utils.common import setMaxFrameRate, overrideMethod, logInfo
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.controllers import msgs_ctrl

BASE_NOTIFICATIONS = (msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND)


class BattleCore(object):

    def __init__(self, config, v_settings):
        self.config = config
        self.v_settings = v_settings
        g_playerEvents.onArenaCreated += self.onArenaCreated
        config.onModSettingsChanged += self.onModSettingsChanged
        overrideMethod(SoundModes, 'setMode')(self.setSoundMode)
        overrideMethod(_ClientArenaVisitor, "hasDogTag")(self.hasDogTag)

    def setSoundMode(self, base, mode, modeName):
        if self.config.main[MAIN.IGNORE_COMMANDERS]:
            if modeName in SOUND_MODES:
                modeName = SoundModes.DEFAULT_MODE_NAME
        return base(mode, modeName)

    def hasDogTag(self, base, *args, **kwargs):
        return False if self.config.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)

    @staticmethod
    def onModSettingsChanged(config, blockID):
        if blockID == MAIN.NAME:
            if config[MAIN.ENABLE_FPS_LIMITER]:
                setMaxFrameRate(config[MAIN.MAX_FRAME_RATE])
            if config[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
                msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
            elif not config[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
                msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND = BASE_NOTIFICATIONS

    def onArenaCreated(self):
        if self.config.log_total[GLOBAL.ENABLED]:
            try:
                dossier = g_currentVehicle.getDossier()
                if dossier:
                    avg = dossier.getRandomStats().getAvgDamage()
                    if avg is not None:
                        avg = round(avg)
                        DAMAGE_LOG.AVG_DAMAGE_DATA = avg
                        logInfo("set vehicle avgDamage: {}".format(avg))
            except AttributeError:
                DAMAGE_LOG.AVG_DAMAGE_DATA = GLOBAL.ZERO
