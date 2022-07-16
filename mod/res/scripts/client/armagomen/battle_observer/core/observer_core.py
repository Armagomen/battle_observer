import sys

from armagomen.battle_observer.core.update.worker import UpdateMain
from armagomen.constants import SWF, MESSAGES, MAIN
from armagomen.utils.common import logInfo, getCurrentModPath, clearClientCache, cleanupUpdates
from constants import ARENA_GUI_TYPE
from gui.Scaleform.daapi.settings import config as packages
from gui.shared.system_factory import registerScaleformBattlePackages

BATTLE_TYPES_TO_INJECT_PACKAGES = {ARENA_GUI_TYPE.RANKED,
                                   ARENA_GUI_TYPE.EPIC_RANDOM,
                                   ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
                                   ARENA_GUI_TYPE.SORTIE_2,
                                   ARENA_GUI_TYPE.FORT_BATTLE_2,
                                   ARENA_GUI_TYPE.TUTORIAL,
                                   ARENA_GUI_TYPE.EPIC_BATTLE}


class ObserverCore(object):
    __slots__ = ("gameVersion", "mod_version")

    def __init__(self, version):
        self.gameVersion = getCurrentModPath()[1]
        self.mod_version = 'v{0} - {1}'.format(version, self.gameVersion)
        update = UpdateMain(version)
        update.subscribe()
        self.start()

    def onExit(self, settings):
        if settings.main[MAIN.AUTO_CLEAR_CACHE]:
            clearClientCache()
        cleanupUpdates()
        logInfo('MOD {0}: {1}'.format(MESSAGES.FINISH, self.mod_version))

    def start(self):
        logInfo("Launched at python " + sys.version)
        logInfo('MOD {0}: {1}'.format(MESSAGES.START, self.mod_version))
        for guiType in BATTLE_TYPES_TO_INJECT_PACKAGES:
            registerScaleformBattlePackages(guiType, SWF.BATTLE_PACKAGES)
        packages.BATTLE_PACKAGES_BY_DEFAULT += SWF.BATTLE_PACKAGES
        packages.LOBBY_PACKAGES += SWF.LOBBY_PACKAGES
