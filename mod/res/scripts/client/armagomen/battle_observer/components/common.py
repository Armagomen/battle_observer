from DogTagComponent import DogTagComponent
from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.core import settings, view_settings
from armagomen.constants import MAIN
from armagomen.utils.common import overrideMethod, getPlayer
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.hint_panel import plugins as hint_plugins
from gui.Scaleform.daapi.view.battle.shared.timers_panel import TimersPanel
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from helpers.func_utils import callback
from messenger.gui.Scaleform.view.battle.messenger_view import BattleMessengerView


# disable field mail tips
@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    if not settings.main[MAIN.FIELD_MAIL]:
        return base(*args)


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    g_events.onHangarVehicleChanged()


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
    if settings.main[MAIN.HIDE_CHAT] and view_settings.isRandomBattle:
        callback(2.0, messanger, "_dispose")


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
