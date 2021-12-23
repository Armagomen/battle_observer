from DogTagComponent import DogTagComponent
from VehicleGunRotator import VehicleGunRotator
from armagomen.battle_observer.core import settings, view_settings
from armagomen.constants import MAIN
from armagomen.utils.common import overrideMethod, getPlayer
from armagomen.utils.events import g_events
from gui.Scaleform.daapi.view.battle.shared.hint_panel import plugins as hint_plugins
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.battle_control.arena_visitor import _ClientArenaVisitor
from gui.game_control.PromoController import PromoController
from gui.game_control.special_sound_ctrl import SpecialSoundCtrl
from messenger.gui.Scaleform.view.battle.messenger_view import BattleMessengerView


@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    if not settings.main[MAIN.FIELD_MAIL]:
        return base(*args)


@overrideMethod(Hangar, "__onCurrentVehicleChanged")
@overrideMethod(Hangar, "__updateAll")
def changeVehicle(base, *args, **kwargs):
    base(*args, **kwargs)
    g_events.onHangarVehicleChanged()


@overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByTankmen")
@overrideMethod(SpecialSoundCtrl, "__setSpecialVoiceByCommanderSkinID")
def setSoundMode(base, *args, **kwargs):
    if settings.main[MAIN.IGNORE_COMMANDERS]:
        return False
    return base(*args, **kwargs)


@overrideMethod(_ClientArenaVisitor, "hasDogTag")
def hasDogTag(base, *args, **kwargs):
    return False if settings.main[MAIN.HIDE_DOG_TAGS] else base(*args, **kwargs)


@overrideMethod(DogTagComponent, "_isObserving")
def _isObservingDogTagFix(*args):
    player = getPlayer()
    return player is None or player.vehicle is None or not player.vehicle.isPlayerVehicle


@overrideMethod(VehicleGunRotator, "__updateGunMarker")
def updateRotationAndGunMarker(base, rotator, *args, **kwargs):
    base(rotator, *args, **kwargs)
    g_events.onDispersionAngleChanged(rotator)


@overrideMethod(BattleMessengerView, "addMessage")
def addMessage(base, *args, **kwargs):
    if settings.main[MAIN.HIDE_CHAT] and view_settings.isRandomBattle:
        return
    return base(*args, **kwargs)


@overrideMethod(hint_plugins, 'createPlugins')
def createPlugins(base, *args, **kwargs):
    result = base(*args, **kwargs)
    if settings.main[MAIN.HIDE_HINT]:
        result.clear()
    return result
