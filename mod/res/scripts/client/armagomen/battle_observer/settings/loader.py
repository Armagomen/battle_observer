import os

from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import LOAD_LIST
from armagomen.utils.common import logWarning, logInfo, writeJsonFile, openJsonFile, logDebug, configsPath
from armagomen.utils.dialogs import LoadingErrorDialog
from armagomen.utils.events import g_events

JSON = "{}.json"
READ_MESSAGE = "SettingsLoader/loadConfigPart: {}: {}"


class SettingsLoader(object):
    __slots__ = ('configName', 'configsList', 'errorMessages')

    def __init__(self):
        self.errorMessages = []
        g_events.onHangarLoaded += self.onHangarLoaded
        load_json = os.path.join(configsPath, 'load.json')
        if os.path.exists(load_json):
            self.configName = openJsonFile(load_json).get('loadConfig')
        else:
            self.configName = 'ERROR_CreatedAutomatically_ERROR'
            configPath = os.path.join(configsPath, self.configName)
            if not os.path.exists(configPath):
                self.errorMessages.append('CONFIGURATION DIRS IS NOT FOUND, CREATE NEW')
                os.makedirs(configPath)
            self.createLoadJSON(self.configName)
            self.errorMessages.append('NEW CONFIGURATION FILE load.json IS CREATED')
        self.readConfig()
        self.configsList = [x for x in os.listdir(configsPath) if os.path.isdir(os.path.join(configsPath, x))]

    def readOtherConfig(self, configID):
        self.configName = self.configsList[configID]
        self.readConfig()
        self.createLoadJSON(self.configName)

    @staticmethod
    def createLoadJSON(configName):
        path = os.path.join(configsPath, 'load.json')
        writeJsonFile(path, {'loadConfig': configName})

    def updateConfigFile(self, fileName, _settings):
        path = os.path.join(configsPath, self.configName, JSON.format(fileName))
        writeJsonFile(path, _settings)

    @staticmethod
    def isNotEqualLen(data1, data2):
        """
        Returns True if the length of 2 dictionaries is not identical,
        or an error occurs when comparing lengths.
        And the settings_core file needs to be rewritten
        """
        if isinstance(data1, dict) and isinstance(data2, dict):
            return len(data1) != len(data2)
        return type(data1) != type(data2)

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        """recursively updates words from settings_core files"""
        file_update |= self.isNotEqualLen(external_cfg, internal_cfg)
        for key in internal_cfg:
            if isinstance(internal_cfg[key], dict):
                file_update |= self.updateData(external_cfg.get(key, {}), internal_cfg[key], file_update)
            else:
                old_param_type = type(internal_cfg[key])
                new_param = external_cfg.get(key)
                if new_param is not None:
                    new_param_type = type(new_param)
                    if new_param_type != old_param_type:
                        file_update = True
                        if old_param_type is int and new_param_type is float:
                            internal_cfg[key] = int(round(new_param))
                        elif old_param_type is float and new_param_type is int:
                            internal_cfg[key] = float(new_param)
                    else:
                        internal_cfg[key] = new_param
                else:
                    file_update = True
        return file_update

    def readConfig(self):
        """Read settings_core file from JSON"""
        logInfo("LOADING USER CONFIGURATION: {}".format(self.configName.upper()))
        direct_path = os.path.join(configsPath, self.configName)
        listdir = os.listdir(direct_path)
        for part_name in LOAD_LIST:
            internal_cfg = getattr(settings, part_name)
            if internal_cfg is None:
                continue
            self.loadConfigPart(part_name, direct_path, listdir, internal_cfg)
        logInfo("LOADING '{}' CONFIGURATION COMPLETED".format(self.configName.upper()))
        settings.onUserConfigUpdateComplete()

    def loadConfigPart(self, part_name, direct_path, listdir, internal_cfg):
        file_name = JSON.format(part_name)
        file_path = os.path.join(direct_path, file_name)
        if file_name not in listdir:
            return writeJsonFile(file_path, internal_cfg)
        try:
            file_data = openJsonFile(file_path)
        except Exception as error:
            message = READ_MESSAGE.format(file_path, repr(error))
            self.errorMessages.append(message)
            return logWarning(message)
        else:
            if self.updateData(file_data, internal_cfg):
                writeJsonFile(file_path, internal_cfg)
            logDebug(READ_MESSAGE, self.configName, file_name)
            settings.onModSettingsChanged(internal_cfg, part_name)

    def onHangarLoaded(self, view):
        if self.errorMessages:
            dialog = LoadingErrorDialog()
            dialog.setView(view)
            dialog.showLoadingError("\n".join(self.errorMessages))
            self.errorMessages = []
