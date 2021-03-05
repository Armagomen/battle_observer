from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from SoundGroups import SoundModes
from gui.Scaleform.daapi.view.battle.shared.postmortem_panel import PostmortemPanel

from armagomen.battle_observer.core.bo_constants import MAIN, SOUND_MODES, GLOBAL, DAMAGE_LOG
from armagomen.battle_observer.core.utils.common import setMaxFrameRate, overrideMethod, logInfo


class BattleCore(object):

    def __init__(self, config):
        self.config = config
        g_playerEvents.onArenaCreated += self.onArenaCreated
        config.onModSettingsChanged += self.onModSettingsChanged

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
            dossier = g_currentVehicle.getDossier()
            if dossier:
                avg = dossier.getRandomStats().getAvgDamage()
                if avg is not None:
                    avg = round(avg)
                    DAMAGE_LOG.AVG_DAMAGE_DATA = avg
                    logInfo("set vehicle avgDamage: {}".format(avg))
