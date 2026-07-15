from sys import version

from armagomen import IALogger
from BattleReplay import isLoading, isPlaying
from helpers import dependency
from realm import CURRENT_REALM


class IBOCore(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError


class Core(IBOCore):
    logger = dependency.descriptor(IALogger)
    isReplay = property(lambda self: isLoading() or isPlaying())

    def __init__(self, modVersion):
        self.logger.logInfo("Initializing Core v{} - Launched at python v{} region={}", modVersion, version, CURRENT_REALM)
        self.version = modVersion
        self.hangar_settings = None
        self.hangar_gf = None

        from armagomen.battle_observer.settings import IBOSettingsLoader
        from armagomen.battle_observer.components import loadComponents
        self.components = loadComponents(self.isReplay)

        settingsLoader = dependency.instance(IBOSettingsLoader)
        settingsLoader.handleModSettingsChangedEvent()

        self.registerBattleObserverPackages()

        if not self.isReplay:
            try:
                from gui.modsListApi import g_modsListApi
                from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
                from armagomen.battle_observer.settings.hangar import SettingsInterface
                api = (g_modsListApi, vxSettingsApi, vxSettingsApiEvents)
            except Exception as error:
                settingsLoader.error_dialog.add(str(error))
                self.logger.logError("Settings Api Not Loaded: {}", str(error))
            else:
                self.hangar_settings = SettingsInterface(self.version, api)

    def fini(self):
        from armagomen.utils.common import cleanupObserverUpdates, cleanupUpdates
        cleanupObserverUpdates()
        cleanupUpdates()
        for component in self.components.values():
            getattr(component, 'fini', lambda: None)()
        if self.hangar_settings is not None:
            self.hangar_settings.fini()
            self.hangar_settings = None
        if self.hangar_gf is not None:
            self.hangar_gf.fini()
            self.hangar_gf = None
        self.logger.logInfo("Finished Core v{}", self.version)

    def registerBattleObserverPackages(self):
        from gui.override_scaleform_views_manager import g_overrideScaleFormViewsConfig
        from gui.Scaleform.required_libraries_config import BATTLE_REQUIRED_LIBRARIES

        if not self.isReplay:
            from armagomen.battle_observer.hangar_gf import HangarGamefaceInject
            self.hangar_gf = HangarGamefaceInject()

        BATTLE_REQUIRED_LIBRARIES.append('modBattleObserver.swf')
        from armagomen._constants import BATTLES_RANGE
        for guiType in BATTLES_RANGE:
            packages = g_overrideScaleFormViewsConfig.battlePackages.setdefault(guiType, [])
            packages.append("armagomen.battle_observer.battle")
