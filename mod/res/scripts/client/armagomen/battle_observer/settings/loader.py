import os

from armagomen._constants import LOAD_LIST, MAIN, SIXTH_SENSE, SNIPER
from armagomen.utils.common import currentConfigPath, openJsonFile, printDebuginfo, SIXTH_SENSE_LIST, writeJsonFile
from armagomen.utils.events import g_events
from armagomen.utils.logging import DEBUG, debug, logError, logInfo, logWarning

JSON = "{}.json"
READ_MESSAGE = "loadConfigPart: {}: {}"


class SettingsLoader(object):
    __slots__ = ('configName', 'configsList', 'errorMessages', '__settings', 'sixth_sense_list', 'error_dialog')

    def __init__(self, settings, errorDialog):
        self.__settings = settings
        self.error_dialog = errorDialog
        self.configsList = sorted(x for x in os.listdir(currentConfigPath) if os.path.isdir(os.path.join(currentConfigPath, x)))
        load_json = os.path.join(currentConfigPath, 'load.json')
        if os.path.isfile(load_json):
            self.configName = openJsonFile(load_json).get('loadConfig')
        else:
            self.configName = self.configsList[0] if self.configsList else 'default'
            self.createLoadJSON(self.configName)
            self.error_dialog.add('NEW CONFIGURATION FILE load.json IS CREATED for {}'.format(self.configName))
            if self.configName not in self.configsList:
                self.configsList.append(self.configName)
        config_path = os.path.join(currentConfigPath, self.configName)
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
            self.error_dialog.add('CONFIGURATION FOLDER {} IS NOT FOUND, CREATE NEW'.format(self.configName))

    @property
    def settings(self):
        return self.__settings

    def readOtherConfig(self, configID):
        if self.configName != self.configsList[configID]:
            self.configName = self.configsList[configID]
            self.createLoadJSON(self.configName)
        self.readConfig()
        self.updateAllSettings()
        return configID

    @staticmethod
    def createLoadJSON(configName):
        path = os.path.join(currentConfigPath, 'load.json')
        writeJsonFile(path, {'loadConfig': configName})

    def updateConfigFile(self, name, data):
        path = os.path.join(currentConfigPath, self.configName, JSON.format(name))
        writeJsonFile(path, data)
        if name == MAIN.NAME and debug.set_debug(data[DEBUG]):
            printDebuginfo()

    @staticmethod
    def isEqualType(data1, data2):
        return type(data1) == type(data2)

    @staticmethod
    def isEqualLen(data1, data2):
        return len(data1) == len(data2)

    @staticmethod
    def isDictAndEquals(data1, data2):
        return isinstance(data1, dict) and isinstance(data2, dict)

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        """Recursively updates values from user settings files"""
        update = not self.isEqualLen(external_cfg, internal_cfg) or file_update

        for key, old_param in internal_cfg.items():
            new_param = external_cfg.get(key)
            if new_param is None or not self.isEqualType(old_param, new_param):
                update = True
                logError("Error in key '{}': parameter values are not compatible. Received: {}, expected: {} - Restore to default", key,
                         new_param, old_param)
                continue
            if key == SIXTH_SENSE.ICON_NAME and new_param not in SIXTH_SENSE_LIST:
                update = True
            elif key == SNIPER.STEPS and (not isinstance(new_param, list) or not len(new_param)):
                update = True
            elif self.isDictAndEquals(old_param, new_param):
                update |= self.updateData(new_param, old_param, file_update=update)
            else:
                internal_cfg[key] = new_param
        return update

    def iterateSettings(self, callback):
        """Process all settings using the provided callback function"""
        for component_name in LOAD_LIST:
            config = getattr(self.__settings, component_name)
            if config is None:
                continue
            callback(component_name, config)

    def readConfig(self):
        """Load user configuration"""
        logInfo("LOADING USER CONFIGURATION: {}", self.configName.upper())
        direct_path = os.path.join(currentConfigPath, self.configName)
        listdir = os.listdir(direct_path)
        self.iterateSettings(lambda name, config_part: self.loadConfigPart(name, direct_path, listdir, config_part))
        logInfo("LOADING '{}' CONFIGURATION COMPLETED", self.configName.upper())

    def updateAllSettings(self):
        """Update all configuration settings"""
        self.iterateSettings(g_events.onModSettingsChanged)

    def loadConfigPart(self, component_name, direct_path, listdir, config):
        """Read settings part file from JSON"""
        file_name = JSON.format(component_name)
        file_path = os.path.join(direct_path, file_name)
        if file_name not in listdir:
            writeJsonFile(file_path, config)
        else:
            try:
                file_data = openJsonFile(file_path)
            except Exception as error:
                message = READ_MESSAGE.format(file_path, repr(error))
                if self.error_dialog:
                    self.error_dialog.add(message)
                logWarning(message)
            else:
                if file_data is not None:
                    if self.updateData(file_data, config):
                        writeJsonFile(file_path, config)
                    logInfo(READ_MESSAGE, self.configName, file_name)
                    if component_name == MAIN.NAME and debug.set_debug(config[DEBUG]):
                        printDebuginfo()
                else:
                    logWarning(READ_MESSAGE, file_name, "file_data is None or file broken")
