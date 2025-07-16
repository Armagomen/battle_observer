import os

from armagomen._constants import GLOBAL, LOAD_LIST, MAIN, SIXTH_SENSE, SNIPER
from armagomen.utils.common import currentConfigPath, openJsonFile, ResMgr, writeJsonFile
from armagomen.utils.dialogs import LoadingErrorDialog
from armagomen.utils.logging import DEBUG, logInfo, logWarning, setDebug
from gui.shared.personality import ServicesLocator

JSON = "{}.json"
READ_MESSAGE = "loadConfigPart: {}: {}"


class SettingsLoader(object):
    __slots__ = ('configName', 'configsList', 'errorMessages', '__settings', 'sixth_sense_list')

    def __init__(self, settings):
        self.__settings = settings
        self.sixth_sense_list = self.sixthSenseIconsNamesList()
        self.errorMessages = set()
        self.configsList = sorted(
            x for x in os.listdir(currentConfigPath) if os.path.isdir(os.path.join(currentConfigPath, x))
        )
        load_json = os.path.join(currentConfigPath, 'load.json')
        if os.path.exists(load_json):
            self.configName = openJsonFile(load_json).get('loadConfig')
        else:
            self.configName = self.configsList[0] if self.configsList else 'default'
            self.createLoadJSON(self.configName)
            self.errorMessages.add('NEW CONFIGURATION FILE load.json IS CREATED for {}'.format(self.configName))
            self.configsList.append(self.configName)
        config_path = os.path.join(currentConfigPath, self.configName)
        if not os.path.exists(config_path):
            self.errorMessages.add('CONFIGURATION FOLDER {} IS NOT FOUND, CREATE NEW'.format(self.configName))
            os.makedirs(config_path)

    @staticmethod
    def sixthSenseIconsNamesList():
        directory = "gui/maps/icons/battle_observer/sixth_sense/"
        folder = ResMgr.openSection(directory)
        return sorted(folder.keys())

    @property
    def settings(self):
        return self.__settings

    def readOtherConfig(self, configID):
        if self.configName != self.configsList[configID]:
            self.configName = self.configsList[configID]
            self.createLoadJSON(self.configName)
        self.readConfig()

    @staticmethod
    def createLoadJSON(configName):
        path = os.path.join(currentConfigPath, 'load.json')
        writeJsonFile(path, {'loadConfig': configName})

    def updateConfigFile(self, data, fileName):
        path = os.path.join(currentConfigPath, self.configName, JSON.format(fileName))
        writeJsonFile(path, data)
        if fileName == MAIN.NAME:
            setDebug(data[DEBUG])

    @staticmethod
    def isNotEqualTypeOrLen(data1, data2):
        """
        Returns True if:
        - data1 and data2 are both dicts but have different lengths
        - or they are of different types
        """
        if isinstance(data1, dict) and isinstance(data2, dict):
            return len(data1) != len(data2)
        return type(data1) != type(data2)

    def updateData(self, external_cfg, internal_cfg, file_update=False):
        """Recursively updates words from user_settings files"""
        update = self.isNotEqualTypeOrLen(external_cfg, internal_cfg) or file_update
        for key in internal_cfg:
            old_param = internal_cfg[key]
            new_param = external_cfg.get(key)
            old_param_type = type(old_param)
            new_param_type = type(new_param)
            if old_param_type == new_param_type == dict:
                update |= self.updateData(external_cfg.get(key, {}), old_param, file_update=update)
            elif self.isNotEqualTypeOrLen(old_param, new_param):
                update = True
                if old_param_type == float and new_param_type == int:
                    internal_cfg[key] = float(new_param)
                continue
            else:
                if key == SIXTH_SENSE.ICON_NAME and new_param not in self.sixth_sense_list:
                    new_param = "logo.png"
                    update = True
                elif key == SNIPER.STEPS and new_param_type != list and not len(new_param):
                    new_param = SNIPER.DEFAULT_STEPS
                    update = True
                elif "statistics_pattern" in key and "WTR" in new_param:
                    new_param = new_param.replace("WTR", "WGR")
                    update = True
                internal_cfg[key] = new_param
        return update

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

    def updateAllSettings(self):
        for part_name in LOAD_LIST:
            internal_cfg = getattr(self.__settings, part_name)
            if internal_cfg is None:
                continue
            self.__settings.onModSettingsChanged(internal_cfg, part_name)

    def loadConfigPart(self, part_name, direct_path, listdir, internal_cfg):
        """Read settings part file from JSON"""
        file_name = JSON.format(part_name)
        file_path = os.path.join(direct_path, file_name)
        if file_name not in listdir:
            writeJsonFile(file_path, internal_cfg)
        else:
            try:
                file_data = openJsonFile(file_path)
            except Exception as error:
                message = READ_MESSAGE.format(file_path, error.message or repr(error))
                self.errorMessages.add(message)
                logWarning(message)
            else:
                if self.updateData(file_data, internal_cfg):
                    writeJsonFile(file_path, internal_cfg)
                logInfo(READ_MESSAGE, self.configName, file_name)
                self.__settings.onModSettingsChanged(internal_cfg, part_name)
                if part_name == MAIN.NAME:
                    setDebug(internal_cfg[DEBUG])

    def onGUISpaceEntered(self, spaceID):
        dialog = LoadingErrorDialog()
        dialog.showLoadingError(GLOBAL.NEW_LINE.join(self.errorMessages))
        self.errorMessages.clear()
        ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
