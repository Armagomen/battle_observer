import os

from armagomen.constants import LOAD_LIST, GLOBAL
from armagomen.utils.common import logWarning, logInfo, getCurrentModPath, createFileInDir, getFileData
from armagomen.utils.dialogs import LoadingErrorDialog
from armagomen.utils.events import g_events


class ConfigLoader(object):
    __slots__ = ('cName', 'path', 'configsList', 'settings', 'errorMessages')

    def __init__(self, settings):
        self.settings = settings
        self.cName = None
        self.path = os.path.join(getCurrentModPath()[GLOBAL.FIRST], "configs", "mod_battle_observer")
        self.configsList = [x for x in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, x))]
        self.errorMessages = []
        self.start()

    @staticmethod
    def makeDirs(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    def start(self):
        """Loading the main settings_core file with the parameters which settings_core to load next"""
        createLoadJson = False
        if self.makeDirs(self.path):
            self.errorMessages.append('CONFIGURATION FILES IS NOT FOUND')
            createLoadJson = True
        else:
            load_json = os.path.join(self.path, 'load.json')
            if os.path.exists(load_json):
                self.cName = getFileData(load_json).get('loadConfig')
            else:
                createLoadJson = True
        if createLoadJson:
            self.cName = self.createLoadJSON(error=True)
            self.makeDirs(os.path.join(self.path, self.cName))
            if self.cName not in self.configsList:
                self.configsList.append(self.cName)
        self.readConfig(self.cName)

    def createLoadJSON(self, cName=None, error=False):
        if cName is None:
            cName = 'ERROR_CreatedAutomatically_ERROR'
        path = os.path.join(self.path, 'load.json')
        createFileInDir(path, {'loadConfig': cName})
        if error:
            self.errorMessages.append('NEW CONFIGURATION FILE load.json IS CREATED')
            return cName

    def updateConfigFile(self, fileName, settings):
        path = os.path.join(self.path, self.cName, '{}.json'.format(fileName))
        createFileInDir(path, settings)

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
                    if new_param_type is str and GLOBAL.REPLACE[GLOBAL.FIRST] in new_param:
                        file_update = True
                        new_param = new_param.replace(*GLOBAL.REPLACE)
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

    def readConfig(self, configName):
        """Read settings_core file from JSON"""
        direct_path = os.path.join(self.path, configName)
        logInfo('START UPDATE USER CONFIGURATION: {}'.format(configName))
        file_list = ['{}.json'.format(name) for name in LOAD_LIST]
        listdir = os.listdir(direct_path)
        for num, module_name in enumerate(LOAD_LIST, GLOBAL.ZERO):
            file_name = file_list[num]
            file_path = os.path.join(direct_path, file_name)
            internal_cfg = getattr(self.settings, module_name)
            if file_name in listdir:
                try:
                    if self.updateData(getFileData(file_path), internal_cfg):
                        createFileInDir(file_path, internal_cfg)
                except Exception as error:
                    self.errorMessages.append(" ".join((file_path, error.message)))
                    logWarning('readConfig: {} {}'.format(file_name, repr(error)))
                    continue
            else:
                createFileInDir(file_path, internal_cfg)
            self.settings.onModSettingsChanged(internal_cfg, module_name)
        logInfo('CONFIGURATION UPDATE COMPLETED: {}'.format(configName))
        self.settings.onUserConfigUpdateComplete()
        if self.errorMessages:
            g_events.onHangarLoaded += self.onHangarLoaded

    def onHangarLoaded(self, view):
        dialog = LoadingErrorDialog()
        dialog.setView(view)
        dialog.showLoadingError("\n".join(self.errorMessages))
        g_events.onHangarLoaded -= self.onHangarLoaded
        del self.errorMessages[:]
