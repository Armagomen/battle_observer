import os

from armagomen import IALogger
from armagomen._constants import ALIAS_TO_CONFIG_NAME_BATTLE, ALIAS_TO_CONFIG_NAME_LOBBY, GLOBAL, LOAD_LIST, MAIN, SIXTH_SENSE, SNIPER
from armagomen.utils.common import clearClientCache, currentConfigPath, openJsonFile, printDebuginfo, SIXTH_SENSE_LIST, writeJsonFile
from armagomen.utils.events import g_events
from Event import Event
from helpers import dependency

JSON = "{}.json"
READ_MESSAGE = "loadConfigPart: {}: {}"


class IBOSettingsLoader(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    @property
    def settings(self):
        raise NotImplementedError

    def readOtherConfig(self, configID):
        raise NotImplementedError

    def createLoadJSON(self, configName):
        raise NotImplementedError

    def updateConfigFile(self, name, data):
        raise NotImplementedError

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        raise NotImplementedError

    def getSettingDictByAliasBattle(self, alias):
        raise NotImplementedError

    def getSettingDictByAliasLobby(self, alias):
        raise NotImplementedError

    def getSetting(self, component_name, param):
        raise NotImplementedError

    def getComponentDict(self, component_name):
        raise NotImplementedError

    def setSetting(self, component_name, key, value):
        raise NotImplementedError


class SettingsLoader(IBOSettingsLoader):
    __slots__ = ('configName', 'load_json', 'configsList', 'errorMessages', '__settings', 'sixth_sense_list', 'error_dialog',
                 '__fini_update', 'onOtherConfigReadComplete')
    logger = dependency.descriptor(IALogger)

    def __init__(self, settings, errorDialog):
        self.logger.logInfo('Initializing SettingsLoader')
        self.onOtherConfigReadComplete = Event()
        self.__settings = settings
        self.error_dialog = errorDialog
        self.configsList = sorted(x for x in os.listdir(currentConfigPath) if os.path.isdir(os.path.join(currentConfigPath, x)))
        self.configName = self.configsList[0] if self.configsList else 'default'
        self.load_json = os.path.join(currentConfigPath, 'load.json')
        self.error_dialog.init()
        self.__fini_update = set()
        self.readConfig()

    def fini(self):
        self.error_dialog.fini()
        self.error_dialog = None
        if self.__settings.main[MAIN.AUTO_CLEAR_CACHE]:
            clearClientCache()
        self.iterateSettings(self.updateConfigFile, self.__fini_update)
        self.__settings = None
        self.__fini_update.clear()
        self.onOtherConfigReadComplete.clear()
        self.onOtherConfigReadComplete = None
        self.logger.logInfo('Finished SettingsLoader')

    @property
    def settings(self):
        return self.__settings

    def addToFiniUpdate(self, component_name):
        self.__fini_update.add(component_name)

    def readOtherConfig(self, configID, reloadConfig=False):
        if self.configName != self.configsList[configID] or reloadConfig:
            self.iterateSettings(self.updateConfigFile, self.__fini_update)
            self.__fini_update.clear()
            self.configName = self.configsList[configID]
            if not reloadConfig:
                self.createLoadJSON(self.configName)
            self.readConfig()
            self.logger.logDebug('SettingsLoader: readOtherConfig={} reload={}', self.configName, reloadConfig)
            self.onOtherConfigReadComplete(configID)

    def createLoadJSON(self, configName):
        writeJsonFile(self.load_json, {'loadConfig': configName})

    def updateConfigFile(self, name, data):
        path = os.path.join(currentConfigPath, self.configName, JSON.format(name))
        writeJsonFile(path, data)

    @staticmethod
    def isEqualType(data1, data2):
        return type(data1) == type(data2)

    @staticmethod
    def isEqualLen(data1, data2):
        return len(data1) == len(data2)

    @staticmethod
    def isDictAndEquals(data1, data2):
        return isinstance(data1, dict) and isinstance(data2, dict)

    def updateData(self, loaded_data, data, file_update=False):
        """Recursively updates values from user settings files"""
        update = not self.isEqualLen(loaded_data, data) or file_update

        for key, param in data.iteritems():
            loaded_param = loaded_data.get(key, None)
            if loaded_param is None or not self.isEqualType(param, loaded_param):
                update = True
                self.logger.logError(
                    "Error in key '{}': parameter values are not compatible. Received: {}, expected: {} - Restore to default", key,
                    loaded_param, param)
                continue
            if key == SIXTH_SENSE.ICON_NAME and loaded_param not in SIXTH_SENSE_LIST:
                update = True
            elif key == SNIPER.STEPS and (not isinstance(loaded_param, list) or not len(loaded_param)):
                update = True
            elif self.isDictAndEquals(param, loaded_param):
                update |= self.updateData(loaded_param, param, file_update=update)
            else:
                data[key] = loaded_param
        return update

    def iterateSettings(self, callback, components):
        """Process list of components using the provided callback function"""
        for component_name in components:
            component = self.getComponentDict(component_name)
            if not component:
                continue
            callback(component_name, component)

    def readConfig(self):
        """Load user configuration"""

        try:
            data = openJsonFile(self.load_json)
        except Exception as error:
            self.logger.logError("Error in openJsonFile: {}", str(error))
            self.createLoadJSON(self.configName)
            self.error_dialog.add('NEW CONFIGURATION FILE load.json IS CREATED for {}'.format(self.configName))
            if self.configName not in self.configsList:
                self.configsList.append(self.configName)
        else:
            self.configName = data.get('loadConfig', self.configName)
        config_path = os.path.join(currentConfigPath, self.configName)
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
            self.error_dialog.add('CONFIGURATION FOLDER {} IS NOT FOUND, CREATE NEW'.format(self.configName))

        self.logger.logInfo("LOADING USER CONFIGURATION: {}", self.configName.upper())
        self.iterateSettings(self.loadConfigPart, LOAD_LIST)
        self.logger.logInfo("LOADING '{}' CONFIGURATION COMPLETED", self.configName.upper())

    def handleModSettingsChangedEvent(self):
        """Update all configuration settings"""
        self.logger.logInfo('HANDLE MOD SETTINGS CHANGED EVENT')
        self.iterateSettings(g_events.onModSettingsChanged, LOAD_LIST)

    def loadConfigPart(self, component_name, data):
        """Read settings part file from JSON"""
        file_name = JSON.format(component_name)
        file_path = os.path.join(currentConfigPath, self.configName, file_name)
        try:
            loaded_data = openJsonFile(file_path)
        except IOError:
            self.addToFiniUpdate(component_name)
        except Exception as error:
            error_message = READ_MESSAGE.format(file_name, str(error))
            if self.error_dialog:
                self.error_dialog.add(error_message)
        else:
            if self.updateData(loaded_data, data):
                self.addToFiniUpdate(component_name)
            if component_name == MAIN.NAME and self.logger.set_debug(data[MAIN.DEBUG]):
                printDebuginfo()

    def getSettingDictByAliasBattle(self, alias):
        # type: (str) -> dict
        return self.getComponentDict(ALIAS_TO_CONFIG_NAME_BATTLE.get(alias, GLOBAL.EMPTY_LINE))

    def getSettingDictByAliasLobby(self, alias):
        # type: (str) -> dict
        return self.getComponentDict(ALIAS_TO_CONFIG_NAME_LOBBY.get(alias, GLOBAL.EMPTY_LINE))

    def getComponentDict(self, component_name):
        component = getattr(self.__settings, component_name, {})
        if not component:
            self.logger.logError("AttributeError: Component * {} * not found in settings", component_name)
        return component

    def getSetting(self, component_name, key=None):
        component = self.getComponentDict(component_name)
        if not component or key is None:
            return component

        param = component.get(key)
        if param is None:
            self.logger.logError("KeyError: Parameter {} not found in {}", key, component_name)
        if isinstance(param, bool):
            param = component.get(GLOBAL.ENABLED, True) and param
        return param

    def setSetting(self, component_name, key, value):
        component = self.getComponentDict(component_name)
        component[key] = value
        self.addToFiniUpdate(component_name)
