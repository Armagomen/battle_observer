import math

from CurrentVehicle import g_currentVehicle
from DogTagComponent import DogTagComponent
from PlayerEvents import g_playerEvents
from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.core import _view_settings
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN, GLOBAL, DAMAGE_LOG
from armagomen.utils.common import overrideMethod, getPlayer, setMaxFrameRate, logDebug, callback
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
from messenger.gui.Scaleform.view.battle.messenger_view import BattleMessengerView


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    callback(1.0, g_events.onVehicleChanged)


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


# fix wg dogTag bug
@overrideMethod(DogTagComponent, "_isObserving")
def _isObservingDogTagFix(*args):
    player = getPlayer()
    return player is None or player.vehicle is None or not player.vehicle.isPlayerVehicle


# update gun dispersion
@overrideMethod(VehicleGunRotator, "__updateGunMarker")
def updateRotationAndGunMarker(base, rotator, *args, **kwargs):
    base(rotator, *args, **kwargs)
    g_events.onDispersionAngleChanged(rotator)


# disable battle chat
@overrideMethod(BattleMessengerView, "_populate")
def messanger_populate(base, messanger):
    base(messanger)
    if settings.main[MAIN.HIDE_CHAT] and _view_settings.isRandomBattle:
        callback(2.0, messanger._dispose)


@overrideMethod(BattleMessengerView, "_dispose")
def messanger_dispose(base, *args):
    try:
        base(*args)
    except AttributeError:
        pass


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


def onArenaCreated():
    if settings.log_total[GLOBAL.ENABLED]:
        try:
            dossier = g_currentVehicle.getDossier()
            if dossier:
                damage = dossier.getRandomStats().getAvgDamage()
                assist = dossier.getRandomStats().getDamageAssistedEfficiencyWithStan()
                if damage is not None:
                    damage = int(math.floor(damage))
                    DAMAGE_LOG.AVG_DAMAGE_DATA = damage
                if assist is not None:
                    assist = int(math.floor(assist))
                    DAMAGE_LOG.AVG_ASSIST_DATA = assist
                logDebug("set vehicle efficiency (avgDamage: {}, avgAssist: {})", damage, assist)
        except AttributeError:
            DAMAGE_LOG.AVG_DAMAGE_DATA = GLOBAL.ZERO


g_playerEvents.onArenaCreated += onArenaCreated
settings.onModSettingsChanged += onModSettingsChanged
