from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN
from armagomen.utils.common import overrideMethod, setMaxFrameRate, callback
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.hint_panel import plugins as hint_plugins
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.Scaleform.daapi.view.meta.LobbyHeaderMeta import LobbyHeaderMeta
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.battle_control.controllers import msgs_ctrl
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from messenger.gui.Scaleform.lobby_entry import LobbyEntry


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    callback(0.6, g_events.onVehicleChanged)


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
@overrideMethod(VehicleGunRotator, "__updateGunMarker")
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


# hide shared chat button
@overrideMethod(LobbyEntry, '__handleLazyChannelCtlInited')
def handleLazyChannelCtlInited(base, entry, event):
    if settings.main[MAIN.HIDE_MAIN_CHAT]:
        ctx = event.ctx
        controller = ctx.get('controller')
        if controller is not None:
            controller.deactivate()
            ctx.clear()
            return
    return base(entry, event)


# hide button counters in lobby header
@overrideMethod(LobbyHeaderMeta, "as_removeButtonCounterS")
@overrideMethod(LobbyHeaderMeta, "as_setButtonCounterS")
def buttonCounterS(base, *args, **kwargs):
    if not settings.main[MAIN.HIDE_BTN_COUNTERS]:
        return base(*args, **kwargs)


BASE_NOTIFICATIONS = (msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND)


def onModSettingsChanged(_settings, blockID):
    if blockID == MAIN.NAME:
        if _settings[MAIN.ENABLE_FPS_LIMITER]:
            setMaxFrameRate(_settings[MAIN.MAX_FRAME_RATE])
        if _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
            msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
        elif not _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
            msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND = BASE_NOTIFICATIONS


settings.onModSettingsChanged += onModSettingsChanged
