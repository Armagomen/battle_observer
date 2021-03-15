from AvatarInputHandler.control_modes import SniperControlMode
from armagomen.battle_observer.core import config
from armagomen.battle_observer.core.bo_constants import EFFECTS
from armagomen.utils.common import overrideMethod
from helpers.EffectsList import EffectsListPlayer


@overrideMethod(SniperControlMode, "__setupBinoculars")
def setupBinoculars(base, mode, isCoatedOptics):
    base(mode, isCoatedOptics)
    if config.effects[EFFECTS.NO_BINOCULARS]:
        mode._binoculars.setEnabled(False)
        mode._binoculars.resetTextures()


@overrideMethod(EffectsListPlayer)
def effectsListPlayer(base, eff, effectsList, keyPoints, **kwargs):
    if EFFECTS.IS_PLAYER_VEHICLE in kwargs:
        if config.effects[EFFECTS.NO_FLASH_BANG] and EFFECTS.SHOW_FLASH_BANG in kwargs:
            kwargs[EFFECTS.SHOW_FLASH_BANG] = False
        if config.effects[EFFECTS.NO_SHOCK_WAVE] and EFFECTS.SHOW_SHOCK_WAVE in kwargs:
            kwargs[EFFECTS.SHOW_SHOCK_WAVE] = False
    # if config.effects[EFFECTS.NO_LIGHT_EFFECT] and 'entity' in kwargs and kwargs['entity'].isPlayerVehicle:
    #     if hasattr(effectsList, '_EffectsList__effectDescList'):
    #         print effectsList, keyPoints
    #         effectsList._EffectsList__effectDescList = \
    #             [e for e in effectsList._EffectsList__effectDescList if e.TYPE != "_PixieEffectDesc"]
    return base(eff, effectsList, keyPoints, **kwargs)
