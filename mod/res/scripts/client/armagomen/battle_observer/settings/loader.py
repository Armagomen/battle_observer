import os

from armagomen._constants import GLOBAL, LOAD_LIST, MAIN, SIXTH_SENSE, SNIPER
from armagomen.utils.common import currentConfigPath, openJsonFile, writeJsonFile
from armagomen.utils.dialogs import LoadingErrorDialog
from armagomen.utils.logging import DEBUG, logInfo, logWarning, setDebug
from gui.shared.personality import ServicesLocator

JSON = "{}.json"
READ_MESSAGE = "loadConfigPart: {}: {}"


class SettingsLoader(object):
    __slots__ = ('configName', 'configsList', 'errorMessages', '__settings')

    def __init__(self, settings):
        self.__settings = settings
        self.errorMessages = []
        self.configsList = sorted(
            x for x in os.listdir(currentConfigPath) if os.path.isdir(os.path.join(currentConfigPath, x))
        )
        load_json = os.path.join(currentConfigPath, 'load.json')
        if os.path.exists(load_json):
            self.configName = openJsonFile(load_json).get('loadConfig')
        else:
            if self.configsList:
                self.configName = self.configsList[0]
            else:
                self.configName = 'default'
            self.createLoadJSON(self.configName)
            self.errorMessages.append('NEW CONFIGURATION FILE load.json IS CREATED for {}'.format(self.configName))
            self.configsList.append(self.configName)
        config_path = os.path.join(currentConfigPath, self.configName)
        if not os.path.exists(config_path):
            self.errorMessages.append('CONFIGURATION FOLDER {} IS NOT FOUND, CREATE NEW'.format(self.configName))
            os.makedirs(config_path)
        self.readConfig()

    def readOtherConfig(self, configID):
        self.configName = self.configsList[configID]
        self.readConfig()
        self.createLoadJSON(self.configName)

    @staticmethod
    def createLoadJSON(configName):
        path = os.path.join(currentConfigPath, 'load.json')
        writeJsonFile(path, {'loadConfig': configName})

    def updateConfigFile(self, fileName, data):
        path = os.path.join(currentConfigPath, self.configName, JSON.format(fileName))
        writeJsonFile(path, data)
        if fileName == MAIN.NAME:
            setDebug(data[DEBUG])

    @staticmethod
    def isNotEqualLen(data1, data2):
        """
        Returns True if the lengths of the 2 dictionaries are not identical,
        or an error occurs when comparing the lengths, and the settings file needs to be rewritten.
        """
        type_1 = type(data1)
        type_2 = type(data2)
        if type_1 == type_2 == dict:
            return len(data1) != len(data2)
        return type_1 != type_2

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        """Recursively updates words from user_settings files"""
        file_update |= self.isNotEqualLen(external_cfg, internal_cfg)
        for key in internal_cfg:
            old_param = internal_cfg[key]
            old_param_type = type(old_param)
            if old_param_type == dict:
                file_update |= self.updateData(external_cfg.get(key, {}), old_param, file_update)
            else:
                new_param = external_cfg.get(key)
                new_param_type = type(new_param)
                file_update |= new_param_type != old_param_type
                if new_param is not None:
                    if old_param_type == float and new_param_type == int:
                        new_param = float(new_param)
                    if key == SIXTH_SENSE.ICON_NAME and new_param not in SIXTH_SENSE.ICONS:
                        new_param = "logo.png"
                        file_update = True
                    if key == SNIPER.STEPS and (new_param_type != list or not len(new_param)):
                        new_param = SNIPER.DEFAULT_STEPS
                        file_update = True
                    internal_cfg[key] = new_param
        return file_update

    def readConfig(self):
        """Read settings"""
        logInfo("LOADING USER CONFIGURATION: {}", self.configName.upper())
        direct_path = os.path.join(currentConfigPath, self.configName)
        listdir = os.listdir(direct_path)
        for part_name in LOAD_LIST:
            internal_cfg = getattr(self.__settings, part_name)
            if internal_cfg is None:
                continue
            self.loadConfigPart(part_name, direct_path, listdir, internal_cfg)
        logInfo("LOADING '{}' CONFIGURATION COMPLETED", self.configName.upper())
        self.__settings.onUserConfigUpdateComplete()
        if self.errorMessages:
            ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def loadConfigPart(self, part_name, direct_path, listdir, internal_cfg):
        """Read settings part file from JSON"""
        file_name = JSON.format(part_name)
        file_path = os.path.join(direct_path, file_name)
        if file_name not in listdir:
            return writeJsonFile(file_path, internal_cfg)
        try:
            file_data = openJsonFile(file_path)
        except Exception as error:
            message = READ_MESSAGE.format(file_path, error.message or repr(error))
            self.errorMessages.append(message)
            return logWarning(message)
        else:
            if self.updateData(file_data, internal_cfg):
                writeJsonFile(file_path, internal_cfg)
            logInfo(READ_MESSAGE, self.configName, file_name)
            self.__settings.onModSettingsChanged(internal_cfg, part_name)
            if part_name == MAIN.NAME:
                setDebug(internal_cfg[DEBUG])

    def onGUISpaceEntered(self, spaceID):
        if self.errorMessages:
            dialog = LoadingErrorDialog()
            dialog.showLoadingError(GLOBAL.NEW_LINE.join(self.errorMessages))
            self.errorMessages = []
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
