from AvatarInputHandler.control_modes import SniperControlMode
from PlayerEvents import g_playerEvents
from helpers.EffectsList import EffectsListPlayer, _PixieEffectDesc
from ..core.bo_constants import EFFECTS
from ..core import cfg, cache
from ..core.utils import overrideMethod


class Effects(object):

    def __init__(self):
        g_playerEvents.onAvatarReady += self.onEnterBattlePage

        @overrideMethod(SniperControlMode, "__setupBinoculars")
        def setupBinoculars(base, mode, isCoatedOptics):
            base(mode, isCoatedOptics)
            if cfg.effects[EFFECTS.NO_BINOCULARS]:
                mode._binoculars.setEnabled(False)
                mode._binoculars.resetTextures()

        @overrideMethod(EffectsListPlayer)
        def effectsListPlayer(base, *args, **kwargs):
            if kwargs.get(EFFECTS.IS_PLAYER_VEHICLE, False):
                if cfg.effects[EFFECTS.NO_FLASH_BANG] and kwargs.get(EFFECTS.SHOW_FLASH_BANG, False):
                    kwargs[EFFECTS.SHOW_FLASH_BANG] = False
                if cfg.effects[EFFECTS.NO_SHOCK_WAVE] and kwargs.get(EFFECTS.SHOW_SHOCK_WAVE, False):
                    kwargs[EFFECTS.SHOW_SHOCK_WAVE] = False
            base(*args, **kwargs)

    @staticmethod
    def onEnterBattlePage():
        if cfg.effects[EFFECTS.NO_LIGHT_EFFECT]:
            gunEffects = cache.player.vehicle.typeDescriptor.gun.effects
            eList = getattr(gunEffects, "effectsList", None)
            if eList is not None and hasattr(eList, "_EffectsList__effectDescList"):
                effectDescList = eList._EffectsList__effectDescList
                eList._EffectsList__effectDescList = \
                    [e for e in effectDescList if not isinstance(e, _PixieEffectDesc)]


effects = Effects()
