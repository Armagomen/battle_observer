from Avatar import PlayerAvatar
from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from SoundGroups import SoundModes
from constants import ARENA_GUI_TYPE
from gui.Scaleform.daapi.view.battle.shared.postmortem_panel import PostmortemPanel
from gui.shared.personality import ServicesLocator
from ..bo_constants import MAIN, SOUND_MODES
from ..config import cfg
from ..events import g_events
from ..utils import overrideMethod
from ..utils.bw_utils import setMaxFrameRate


class _BattleCore(object):

    def __init__(self, cache):
        self.load_health_module = False
        self.callbackTime = 0.01
        self.cache = cache
        g_playerEvents.onArenaCreated += self.onArenaCreated
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        g_events.onSettingsChanged += self.onSettingsChanged

    @staticmethod
    @overrideMethod(PlayerAvatar, "showTracer")
    def showTracer(base, avatar, shooterID, *args):
        if shooterID == avatar.playerVehicleID:
            g_events.onPlayerShooting(avatar)
        return base(avatar, shooterID, *args)

    @staticmethod
    @overrideMethod(PlayerAvatar, "getOwnVehicleShotDispersionAngle")
    def getOwnVehicleShotDispersionAngle(base, *args, **kwargs):
        dispersion_angle = base(*args, **kwargs)
        g_events.onDispersionAngleUpdate(dispersion_angle[0])
        return dispersion_angle

    @staticmethod
    @overrideMethod(PostmortemPanel, "getDeathInfo")
    def getDeathInfo(info, *args, **kwargs):
        if cfg.main[MAIN.HIDE_POSTMORTEM_TIPS]:
            return None
        return info(*args, **kwargs)

    @staticmethod
    def onSettingsChanged(config, blockID):
        if blockID == MAIN.NAME and config[MAIN.ENABLE_FPS_LIMITER]:
            setMaxFrameRate(config[MAIN.MAX_FRAME_RATE])

    def onArenaCreated(self):
        intCD = getattr(g_currentVehicle.item, "intCD", None)
        if intCD:
            avg = ServicesLocator.itemsCache.items.getVehicleDossier(intCD).getRandomStats().getAvgDamage()
            if avg is not None:
                self.cache.tankAvgDamage = float(avg)

    def isAllowedBattleType(self, arenaVisitor=None):
        enabled = False
        if arenaVisitor is None:
            arenaVisitor = self.cache.getArenaVisitor()
        if arenaVisitor is not None:
            enabled = arenaVisitor.gui.isRandomBattle() or \
                      arenaVisitor.gui.isTrainingBattle() or \
                      arenaVisitor.gui.isRankedBattle() or \
                      arenaVisitor.getArenaGuiType() in (ARENA_GUI_TYPE.UNKNOWN,
                                                         ARENA_GUI_TYPE.FORT_BATTLE_2,
                                                         ARENA_GUI_TYPE.SORTIE_2)
        return enabled, arenaVisitor

    @staticmethod
    @overrideMethod(SoundModes, 'setMode')
    def setSoundMode(base, mode, modeName):
        if cfg.main[MAIN.IGNORE_COMMANDERS]:
            if modeName in SOUND_MODES:
                modeName = SoundModes.DEFAULT_MODE_NAME
        return base(mode, modeName)

    def onEnterBattlePage(self):
        enabled, arenaVisitor = self.isAllowedBattleType()
        if enabled and arenaVisitor is not None:
            arena = arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleKilled += self.onVehicleKilled
                arena.onVehicleAdded += self.onVehicleAddUpdate
                arena.onVehicleUpdated += self.onVehicleAddUpdate

    def onExitBattlePage(self):
        enabled, arenaVisitor = self.isAllowedBattleType()
        if enabled and arenaVisitor is not None:
            arena = arenaVisitor.getArenaSubscription()
            if arena is not None:
                arena.onVehicleKilled -= self.onVehicleKilled
                arena.onVehicleAdded -= self.onVehicleAddUpdate
                arena.onVehicleUpdated -= self.onVehicleAddUpdate

    def onVehicleKilled(self, targetID, attackerID, *args, **kwargs):
        if self.cache.player.playerVehicleID == targetID:
            g_events.onPlayerVehicleDeath(attackerID)
        elif self.cache.player.playerVehicleID == attackerID:
            g_events.onPlayerKilledEnemy(targetID)

    def onVehicleAddUpdate(self, vehicleID, *args, **kwargs):
        vehicleInfoVO = self.cache.arenaDP.getVehicleInfo(vehicleID)
        if vehicleInfoVO:
            vehicleType = vehicleInfoVO.vehicleType
            if vehicleType and vehicleType.maxHealth and vehicleType.classTag:
                g_events.onVehicleAddUpdate(vehicleID, vehicleType)
