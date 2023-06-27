from CurrentVehicle import g_currentVehicle
from VehicleGunRotator import VehicleGunRotator
from armagomen._constants import MAIN
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import overrideMethod, callback
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.hint_panel import plugins as hint_plugins
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.controllers import msgs_ctrl
from gui.battle_control.controllers.sound_ctrls.comp7_battle_sounds import _EquipmentZoneSoundPlayer
from gui.battle_control.controllers.team_bases_ctrl import BattleTeamsBasesController
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from messenger.gui.Scaleform.lobby_entry import LobbyEntry


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    g_events.onVehicleChanged()
    callback(1.0, g_events.onVehicleChangedDelayed, g_currentVehicle.item)


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    if not settings.main[MAIN.FIELD_MAIL]:
        return base(*args)


# disable commander voices
@overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByTankmen")
@overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByCommanderSkinID")
def setSoundMode(base, *args, **kwargs):
    if settings.main[MAIN.IGNORE_COMMANDERS]:
        return False
    return base(*args, **kwargs)


# disable dogTag
@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)


# update gun dispersion
@overrideMethod(VehicleGunRotator, "updateRotationAndGunMarker")
def updateRotationAndGunMarker(base, rotator, *args, **kwargs):
    base(rotator, *args, **kwargs)
    g_events.onDispersionAngleChanged(rotator)


# disable battle hints
@overrideMethod(hint_plugins, "createPlugins")
def createPlugins(base, *args, **kwargs):
    result = base(*args, **kwargs)
    if settings.main[MAIN.HIDE_HINT]:
        result.clear()
    return result


# disable battle artillery_stun_effect sound
@overrideMethod(TimersPanel, "__playStunSoundIfNeed")
def playStunSoundIfNeed(base, *args, **kwargs):
    if not settings.main[MAIN.STUN_SOUND]:
        return base(*args, **kwargs)


@overrideMethod(_EquipmentZoneSoundPlayer, "_onVehicleStateUpdated")
def _onVehicleStateUpdated(base, eq, state, value):
    if state == VEHICLE_VIEW_STATE.STUN and settings.main[MAIN.STUN_SOUND]:
        return
    return base(eq, state, value)


# hide shared chat button
@overrideMethod(LobbyEntry, '__handleLazyChannelCtlInited')
def handleLazyChannelCtlInited(base, entry, event):
    if settings.main[MAIN.HIDE_MAIN_CHAT]:
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
@overrideMethod(LobbyHeader, "as_removeButtonCounterS")
@overrideMethod(LobbyHeader, "as_setButtonCounterS")
def buttonCounterS(base, *args, **kwargs):
    if not settings.main[MAIN.HIDE_BTN_COUNTERS]:
        return base(*args, **kwargs)


def onModSettingsChanged(_settings, blockID):
    if blockID == MAIN.NAME:
        if _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
            msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
        elif not _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
            msgs_ctrl._ALLY_KILLED_SOUND = 'ally_killed_by_enemy'
            msgs_ctrl._ENEMY_KILLED_SOUND = 'enemy_killed_by_ally'


@overrideMethod(BattleTeamsBasesController, "__playCaptureSound")
def muteCaptureSound(base, *args):
    if not settings.main[MAIN.MUTE_BASES_SOUND]:
        return base(*args)


settings.onModSettingsChanged += onModSettingsChanged
