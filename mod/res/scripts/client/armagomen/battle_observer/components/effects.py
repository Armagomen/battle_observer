from armagomen._constants import EFFECTS
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import overrideMethod
from AvatarInputHandler.control_modes import SniperControlMode
from helpers import dependency
from helpers.bound_effects import ModelBoundEffects


class Effects(object):
    settingsLoder = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        overrideMethod(SniperControlMode, "__setupBinoculars")(self.setupBinoculars)
        overrideMethod(ModelBoundEffects, 'addNewToNode')(self.effectsListPlayer)

    def setupBinoculars(self, base, mode, optDevices):
        if not self.settingsLoder.getSetting(EFFECTS.NAME, EFFECTS.NO_BINOCULARS):
            return base(mode, optDevices)
        return None

    def effectsListPlayer(self, base, *args, **kwargs):
        if EFFECTS.IS_PLAYER_VEHICLE in kwargs:
            if self.settingsLoder.getSetting(EFFECTS.NAME, EFFECTS.NO_FLASH_BANG) and EFFECTS.SHOW_FLASH_BANG in kwargs:
                kwargs[EFFECTS.SHOW_FLASH_BANG] = False
            if self.settingsLoder.getSetting(EFFECTS.NAME, EFFECTS.NO_SHOCK_WAVE) and EFFECTS.SHOW_SHOCK_WAVE in kwargs:
                kwargs[EFFECTS.SHOW_SHOCK_WAVE] = False
        return base(*args, **kwargs)


effects = Effects()
