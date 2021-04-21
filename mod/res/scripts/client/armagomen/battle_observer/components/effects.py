from AvatarInputHandler.control_modes import SniperControlMode
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.core.bo_constants import EFFECTS
from armagomen.utils.common import overrideMethod
from helpers.bound_effects import ModelBoundEffects


@overrideMethod(SniperControlMode, "__setupBinoculars")
def setupBinoculars(base, mode, isCoatedOptics):
    base(mode, isCoatedOptics)
    if settings.effects[EFFECTS.NO_BINOCULARS]:
        mode._binoculars.setEnabled(False)
        mode._binoculars.resetTextures()


@overrideMethod(ModelBoundEffects, 'addNewToNode')
def effectsListPlayer(base, *args, **kwargs):
    if EFFECTS.IS_PLAYER_VEHICLE in kwargs:
        if settings.effects[EFFECTS.NO_FLASH_BANG] and EFFECTS.SHOW_FLASH_BANG in kwargs:
            kwargs[EFFECTS.SHOW_FLASH_BANG] = False
        if settings.effects[EFFECTS.NO_SHOCK_WAVE] and EFFECTS.SHOW_SHOCK_WAVE in kwargs:
            kwargs[EFFECTS.SHOW_SHOCK_WAVE] = False
    return base(*args, **kwargs)
