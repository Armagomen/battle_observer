from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from SoundGroups import SoundModes
from gui.Scaleform.daapi.view.battle.shared.postmortem_panel import PostmortemPanel
from gui.shared.personality import ServicesLocator
from ..bo_constants import MAIN, SOUND_MODES, GLOBAL
from ..utils.common import setMaxFrameRate, overrideMethod


class BattleCore(object):

    def __init__(self, config, cache):
        self.load_health_module = False
        self.callbackTime = 0.01
        self.cache = cache
        self.config = config
        g_playerEvents.onArenaCreated += self.onArenaCreated
        cache.onModSettingsChanged += self.onModSettingsChanged

        @overrideMethod(PostmortemPanel, "getDeathInfo")
        def getDeathInfo(info, *args, **kwargs):
            if config.main[MAIN.HIDE_POSTMORTEM_TIPS]:
                return None
            return info(*args, **kwargs)

        @overrideMethod(SoundModes, 'setMode')
        def setSoundMode(base, mode, modeName):
            if config.main[MAIN.IGNORE_COMMANDERS]:
                if modeName in SOUND_MODES:
                    modeName = SoundModes.DEFAULT_MODE_NAME
            return base(mode, modeName)

    @staticmethod
    def onModSettingsChanged(config, blockID):
        if blockID == MAIN.NAME and config[MAIN.ENABLE_FPS_LIMITER]:
            setMaxFrameRate(config[MAIN.MAX_FRAME_RATE])

    def onArenaCreated(self):
        if self.config.log_total[GLOBAL.ENABLED]:
            intCD = getattr(g_currentVehicle.item, "intCD", None)
            if intCD:
                avg = ServicesLocator.itemsCache.items.getVehicleDossier(intCD).getRandomStats().getAvgDamage()
                if avg is not None:
                    self.cache.tankAvgDamage = float(avg)
