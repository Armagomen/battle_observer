from armagomen._constants import IS_WG_CLIENT, MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, overrideMethod
from armagomen.utils.events import g_events
from CurrentVehicle import g_currentVehicle
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers import msgs_ctrl
from gui.battle_control.controllers.team_bases_ctrl import BattleTeamsBasesController
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.lobby.hangar.entry_points.event_entry_points_container import EventEntryPointsContainer
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from messenger.gui.Scaleform.lobby_entry import LobbyEntry


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    addCallback(0.2, g_events.onVehicleChangedDelayed, g_currentVehicle.item)


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    return None if user_settings.main[MAIN.FIELD_MAIL] else base(*args)


@overrideMethod(PromoController, "__needToGetTeasersInfo")
def __needToGetTeasersInfo(base, *args):
    return False if user_settings.main[MAIN.FIELD_MAIL] else base(*args)


# disable dogTag
@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if user_settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)


# hide shared chat button
@overrideMethod(LobbyEntry, '__handleLazyChannelCtlInited')
def handleLazyChannelCtlInited(base, entry, event):
    if user_settings.main[MAIN.HIDE_MAIN_CHAT]:
        ctx = event.ctx
        controller = ctx.get('controller')
        if controller is not None:
            channel = controller.getChannel()
            controller.deactivate()
            ctx.clear()
            entry._LobbyEntry__carouselHandler.removeChannel(channel)
            return
    return base(entry, event)


# hide button counters in lobby header
@overrideMethod(LobbyHeader, "__setCounter")
def buttonCounterS(base, *args, **kwargs):
    return None if user_settings.main[MAIN.HIDE_BTN_COUNTERS] else base(*args, **kwargs)


class PrestigeWidget(object):

    def __init__(self):
        from gui.Scaleform.daapi.view.lobby.profile.ProfileTechnique import ProfileTechnique
        self.enabled = False
        overrideMethod(Hangar, 'as_setPrestigeWidgetVisibleS')(self.as_setPrestigeWidgetVisibleS)
        overrideMethod(ProfileTechnique, 'as_setPrestigeVisibleS')(self.as_setPrestigeVisibleS)
        user_settings.onModSettingsChanged += self.onModSettingsChanged

    @staticmethod
    def as_setPrestigeWidgetVisibleS(base, hangar, value):
        return base(hangar, False if user_settings.main[MAIN.HIDE_PRESTIGE_HANGAR_WIDGET] else value)

    @staticmethod
    def as_setPrestigeVisibleS(base, profile, value):
        return base(profile, False if user_settings.main[MAIN.HIDE_PRESTIGE_PROFILE_WIDGET] else value)

    def onModSettingsChanged(self, settings, blockID):
        if blockID != MAIN.NAME:
            return
        enabled = settings[MAIN.HIDE_PRESTIGE_HANGAR_WIDGET]
        if self.enabled != enabled and g_currentVehicle.intCD:
            self.enabled = enabled
            g_currentVehicle.onChanged()


@overrideMethod(EventEntryPointsContainer, 'as_updateEntriesS')
def _EventEntryPointsContainer_as_updateEntries(base, self, data):
    return base(self, [] if user_settings.main[MAIN.HIDE_EVENT_BANNER] else data)


if IS_WG_CLIENT:
    p_widget = PrestigeWidget()
    from comp7.gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds import _EquipmentZoneSoundPlayer
    from gui.Scaleform.daapi.view.battle.shared.hint_panel import BattleHintPanel
else:
    from gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds import _EquipmentZoneSoundPlayer
    from gui.Scaleform.daapi.view.battle.shared.hint_panel.component import BattleHintPanel


# disable battle hints
@overrideMethod(BattleHintPanel, "_initPlugins")
def _initPlugins(base, *args, **kwargs):
    if not user_settings.main[MAIN.HIDE_HINT]:
        base(*args, **kwargs)


class TweakSounds(object):

    def __init__(self):
        user_settings.onModSettingsChanged += self.onModSettingsChanged

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
    @overrideMethod(_EquipmentZoneSoundPlayer, "_onVehicleStateUpdated")
    def _onVehicleStateUpdated(base, eq, state, value):
        if state == VEHICLE_VIEW_STATE.STUN and user_settings.main[MAIN.STUN_SOUND]:
            return
        return base(eq, state, value)

    @staticmethod
    def onModSettingsChanged(settings, blockID):
        if blockID != MAIN.NAME:
            return
        if settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
            msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
        elif not settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
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


t_sounds = TweakSounds()


def fini():
    user_settings.onModSettingsChanged -= t_sounds.onModSettingsChanged
    if IS_WG_CLIENT:
        user_settings.onModSettingsChanged -= p_widget.onModSettingsChanged
