from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from armagomen.utils.events import g_events
from comp7_core.gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds import _EquipmentZoneSoundPlayer
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers import msgs_ctrl
from gui.battle_control.controllers.team_bases_ctrl import BattleTeamsBasesController
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from gui.Scaleform.daapi.view.battle.shared.hint_panel import BattleHintPanel
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel


# disable battle hints
@overrideMethod(BattleHintPanel, "_initPlugins")
def _initPlugins(base, panel, *args, **kwargs):
    if not user_settings.main[MAIN.HIDE_HINT]:
        base(panel, *args, **kwargs)
    elif panel._plugins is not None:
        panel._plugins.stop()
        panel._plugins.fini()
        panel._plugins = None


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def _tryToShowTeaser(base, *args):
    return None if user_settings.main[MAIN.FIELD_MAIL] else base(*args)


@overrideMethod(PromoController, "__needToGetTeasersInfo")
def _needToGetTeasersInfo(base, *args):
    return False if user_settings.main[MAIN.FIELD_MAIL] else base(*args)


# disable dogTag
@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if user_settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)


class TweakSounds(object):

    def __init__(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def fini(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    @staticmethod
    @overrideMethod(BattleTeamsBasesController, "__playCaptureSound")
    def muteCaptureSound(base, *args):
        if not user_settings.main[MAIN.MUTE_BASES_SOUND]:
            return base(*args)

    # disable battle artillery_stun_effect sound
    @staticmethod
    @overrideMethod(TimersPanel, "__playStunSoundIfNeed")
    def playStunSoundIfNeed(base, *args, **kwargs):
        if not user_settings.main[MAIN.STUN_SOUND]:
            return base(*args, **kwargs)

    @staticmethod
    def onModSettingsChanged(name, data):
        if name != MAIN.NAME:
            return
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
        if user_settings.main[MAIN.IGNORE_COMMANDERS]:
            return False
        return base(*args, **kwargs)

    @staticmethod
    @overrideMethod(_EquipmentZoneSoundPlayer, "_onVehicleStateUpdated")
    def _onVehicleStateUpdated(base, eq, state, value):
        if state == VEHICLE_VIEW_STATE.STUN and user_settings.main[MAIN.STUN_SOUND]:
            return
        return base(eq, state, value)


t_sounds = TweakSounds()


def fini():
    t_sounds.fini()
