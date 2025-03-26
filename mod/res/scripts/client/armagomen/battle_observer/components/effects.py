from armagomen._constants import EFFECTS
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from AvatarInputHandler.control_modes import SniperControlMode
from helpers.bound_effects import ModelBoundEffects


@overrideMethod(SniperControlMode, "__setupBinoculars")
def setupBinoculars(base, mode, optDevices):
    if not user_settings.effects[EFFECTS.NO_BINOCULARS]:
        return base(mode, optDevices)


@overrideMethod(ModelBoundEffects, 'addNewToNode')
def effectsListPlayer(base, *args, **kwargs):
    if EFFECTS.IS_PLAYER_VEHICLE in kwargs:
        if user_settings.effects[EFFECTS.NO_FLASH_BANG] and EFFECTS.SHOW_FLASH_BANG in kwargs:
            kwargs[EFFECTS.SHOW_FLASH_BANG] = False
        if user_settings.effects[EFFECTS.NO_SHOCK_WAVE] and EFFECTS.SHOW_SHOCK_WAVE in kwargs:
            kwargs[EFFECTS.SHOW_SHOCK_WAVE] = False
    return base(*args, **kwargs)
