from armagomen._constants import MAIN
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import overrideMethod, safe_import
from armagomen.utils.events import g_events
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers import msgs_ctrl
from gui.battle_control.controllers.team_bases_ctrl import BattleTeamsBasesController
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from gui.Scaleform.daapi.view.battle.shared.hint_panel import BattleHintPanel
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from helpers import dependency

settingsLoader = dependency.instance(IBOSettingsLoader)

_EquipmentZoneSoundPlayer = safe_import((
    ("comp7_core.gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds", "_EquipmentZoneSoundPlayer"),
), noneResults=True)[0]

if _EquipmentZoneSoundPlayer:
    @overrideMethod(_EquipmentZoneSoundPlayer, "_onVehicleStateUpdated")
    def _onVehicleStateUpdated(base, eq, state, value):
        if state == VEHICLE_VIEW_STATE.STUN and settingsLoader.getSetting(MAIN.NAME, MAIN.STUN_SOUND):
            return None
        return base(eq, state, value)


# disable battle hints
@overrideMethod(BattleHintPanel, "_initPlugins")
def _initPlugins(base, panel, *args, **kwargs):
    if not settingsLoader.getSetting(MAIN.NAME, MAIN.HIDE_HINT):
        base(panel, *args, **kwargs)
    elif panel._plugins is not None:
        panel._plugins.stop()
        panel._plugins.fini()
        panel._plugins = None


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def _tryToShowTeaser(base, *args):
    return None if settingsLoader.getSetting(MAIN.NAME, MAIN.FIELD_MAIL) else base(*args)


@overrideMethod(PromoController, "__needToGetTeasersInfo")
def _needToGetTeasersInfo(base, *args):
    return False if settingsLoader.getSetting(MAIN.NAME, MAIN.FIELD_MAIL) else base(*args)


# disable dogTag
@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if settingsLoader.getSetting(MAIN.NAME, MAIN.HIDE_DOG_TAGS) else base(*args, **kwargs)


class TweakSounds(object):

    def __init__(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def fini(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    @staticmethod
    @overrideMethod(BattleTeamsBasesController, "__playCaptureSound")
    def muteCaptureSound(base, *args):
        if not settingsLoader.getSetting(MAIN.NAME, MAIN.MUTE_BASES_SOUND):
            return base(*args)
        return None

    # disable battle artillery_stun_effect sound
    @staticmethod
    @overrideMethod(TimersPanel, "__playStunSoundIfNeed")
    def playStunSoundIfNeed(base, *args, **kwargs):
        if not settingsLoader.getSetting(MAIN.NAME, MAIN.STUN_SOUND):
            return base(*args, **kwargs)
        return None

    @staticmethod
    def onModSettingsChanged(name, data):
        if name != MAIN.NAME:
            return
        if MAIN.DISABLE_SCORE_SOUND in data:
            if data[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
                msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
            elif not data[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
                msgs_ctrl._ALLY_KILLED_SOUND = 'ally_killed_by_enemy'
                msgs_ctrl._ENEMY_KILLED_SOUND = 'enemy_killed_by_ally'

    # disable commander voices
    @staticmethod
    @overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByTankmen")
    @overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByCommanderSkinID")
    def setSoundMode(base, *args, **kwargs):
        if settingsLoader.getSetting(MAIN.NAME, MAIN.IGNORE_COMMANDERS):
            return False
        return base(*args, **kwargs)


t_sounds = TweakSounds()


def fini():
    t_sounds.fini()
