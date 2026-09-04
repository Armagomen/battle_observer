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

    def updateData(self, loaded_data, data, file_update=False):
        raise NotImplementedError

    def getSettingDictByAliasBattle(self, alias):
        raise NotImplementedError

    def getSettingDictByAliasLobby(self, alias):
        raise NotImplementedError

    def getSetting(self, component_name, key=None):
        raise NotImplementedError

    def getComponentDict(self, component_name):
        raise NotImplementedError

    def setSetting(self, component_name, key, value):
        raise NotImplementedError
