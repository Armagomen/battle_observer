class IBOSettingsLoader(object):
    __slots__ = ()

    def init(self):
        raise NotImplementedError

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

    def updateAllSettings(self):
        raise NotImplementedError

    def getSettingDictByAliasBattle(self, alias):
        raise NotImplementedError

    def getSettingDictByAliasLobby(self, alias):
        raise NotImplementedError

    def getSetting(self, component_name, param):
        raise NotImplementedError