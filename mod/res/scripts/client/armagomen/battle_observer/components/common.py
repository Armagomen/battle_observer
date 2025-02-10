from armagomen._constants import MAIN
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import addCallback, overrideMethod
from armagomen.utils.events import g_events
from CurrentVehicle import g_currentVehicle
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers import msgs_ctrl
from gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds import _EquipmentZoneSoundPlayer
from gui.battle_control.controllers.team_bases_ctrl import BattleTeamsBasesController
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from gui.Scaleform.daapi.view.battle.shared.hint_panel import plugins as hint_plugins
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.lobby.hangar.entry_points.event_entry_points_container import EventEntryPointsContainer
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from gui.Scaleform.daapi.view.lobby.profile.ProfileTechnique import ProfileTechnique
from messenger.gui.Scaleform.lobby_entry import LobbyEntry


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    g_events.onVehicleChanged()
    addCallback(1.0, g_events.onVehicleChangedDelayed, g_currentVehicle.item)


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    if not user_settings.main[MAIN.FIELD_MAIL]:
        return base(*args)


# disable dogTag
@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if user_settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)


# disable battle hints
@overrideMethod(hint_plugins, "createPlugins")
def createPlugins(base, *args, **kwargs):
    result = base(*args, **kwargs)
    if user_settings.main[MAIN.HIDE_HINT]:
        result.clear()
    return result


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
    if not user_settings.main[MAIN.HIDE_BTN_COUNTERS]:
        return base(*args, **kwargs)


class PrestigeWidget(object):

    def __init__(self):
        self.enabled = False

    @staticmethod
    @overrideMethod(Hangar, 'as_setPrestigeWidgetVisibleS')
    def as_setPrestigeWidgetVisibleS(base, self, value):
        if user_settings.main[MAIN.HIDE_PRESTIGE_HANGAR_WIDGET]:
            value = False
        return base(self, value)

    @staticmethod
    @overrideMethod(ProfileTechnique, 'as_setPrestigeVisibleS')
    def as_setPrestigeVisibleS(base, self, value):
        if user_settings.main[MAIN.HIDE_PRESTIGE_PROFILE_WIDGET]:
            value = False
        return base(self, value)

    @staticmethod
    @overrideMethod(EventEntryPointsContainer, 'as_updateEntriesS')
    def _EventEntryPointsContainer_as_updateEntries(base, self, data):
        if user_settings.main[MAIN.HIDE_EVENT_BANNER]:
            return base(self, [])
        return base(self, data)

    def update(self, settings):
        enabled = any((settings[MAIN.HIDE_PRESTIGE_HANGAR_WIDGET], settings[MAIN.HIDE_PRESTIGE_PROFILE_WIDGET],
                       settings[MAIN.HIDE_EVENT_BANNER]))
        if self.enabled != enabled and g_currentVehicle.intCD:
            self.enabled = enabled
            g_currentVehicle.onChanged()


p_widget = PrestigeWidget()


class TweakSounds(object):

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
    def updateKilledSounds(settings):
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


def _onModSettingsChanged(settings, blockID):
    if blockID == MAIN.NAME:
        t_sounds.updateKilledSounds(settings)
        p_widget.update(settings)


user_settings.onModSettingsChanged += _onModSettingsChanged


def fini():
    user_settings.onModSettingsChanged -= _onModSettingsChanged
