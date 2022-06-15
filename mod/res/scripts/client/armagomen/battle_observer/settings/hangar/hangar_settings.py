# coding=utf-8
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import GLOBAL, CONFIG_INTERFACE, HP_BARS, DISPERSION, SNIPER, MOD_NAME, MAIN, \
    ANOTHER, URLS, STATISTICS, PANELS, MINIMAP
from armagomen.utils.common import logWarning, openWebBrowser, logInfo
from bwobsolete_helpers.BWKeyBindings import KEY_ALIAS_CONTROL, KEY_ALIAS_ALT
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.shared.personality import ServicesLocator
from gui.shared.utils.functions import makeTooltip
from skeletons.gui.app_loader import GuiGlobalSpaceID

settingsVersion = 37
KEY_CONTROL = [KEY_ALIAS_CONTROL]
KEY_ALT = [KEY_ALIAS_ALT]

LOCKED_BLOCKS = (STATISTICS.NAME, PANELS.PANELS_NAME, MINIMAP.NAME)
LOCKED = ("<font color='#ff3d3d'> The function is not available, XVM is installed.</font>",
          "<font color='#ff3d3d'> Функция недоступна, установлен XVM.</font>")


class CreateElement(object):

    def __init__(self):
        self.settings = None
        self.getter = None

    @staticmethod
    def createLabel(blockID, name):
        block = localization.get(blockID, {})
        if name not in block:
            return None
        return {
            'type': 'Label', 'text': block[name],
            'tooltip': makeTooltip(block[name], block.get('{}_tooltip'.format(name))),
            'tooltipIcon': 'no_icon'
        }

    @staticmethod
    def createEmpty():
        return {'type': 'Empty'}

    @staticmethod
    def getControlType(value, cType):
        if cType is None:
            if isinstance(value, str):
                if value.startswith("#"):
                    return 'TextInputColor'
                return 'TextInputField'
            elif type(value) is bool:
                return 'CheckBox'
        else:
            return cType

    def createControl(self, blockID, varName, value, cType=None):
        result = self.createLabel(blockID, varName)
        if result is not None:
            result.update({'type': self.getControlType(value, cType), 'value': value, 'varName': varName,
                           GLOBAL.WIDTH: 350, 'defaultSelection': False})
            if cType == 'Button':
                result.update({GLOBAL.WIDTH: 250, 'btnName': varName})
        return result

    def createDropDown(self, blockID, varName, options, value):
        result = self.createControl(blockID, varName, value, cType='Dropdown')
        if result is not None:
            result.update({'options': [{'label': x} for x in options]})
        return result

    def createRadioButtonGroup(self, blockID, varName, options, value):
        result = self.createDropDown(blockID, varName, options, value)
        if result is not None:
            result.update(type="RadioButtonGroup")
        return result

    def createHotKey(self, blockID, varName, value, defaultValue):
        result = self.createControl(blockID, varName, value, cType='KeyInput')
        if result is not None:
            result['defaultValue'] = defaultValue
        return result

    def __createNumeric(self, blockID, varName, cType, value, vMin=GLOBAL.ZERO, vMax=GLOBAL.ZERO):
        result = self.createControl(blockID, varName, value, cType=cType)
        if result is not None:
            result.update({'minimum': vMin, 'maximum': vMax})
        return result

    def createStepper(self, blockID, varName, vMin, vMax, step, value):
        result = self.__createNumeric(blockID, varName, 'NumericStepper', value, vMin, vMax)
        if result is not None:
            result.update({'stepSize': step, 'canManualInput': True})
        return result

    def createSlider(self, blockID, varName, vMin, vMax, step, value):
        result = self.__createNumeric(blockID, varName, 'Slider', value, vMin, vMax)
        if result is not None:
            result.update({'snapInterval': step, 'format': '{{value}}'})
        return result

    def createBlock(self, blockID, settings, column1, column2):
        name = localization.get(blockID, {}).get("header", blockID)
        warning = self.settings.xvmInstalled and blockID in LOCKED_BLOCKS
        if warning:
            name += LOCKED[GLOBAL.RU_LOCALIZATION]
        return {
            'modDisplayName': "<font color='#FFFFFF'>{}</font>".format(name),
            'settingsVersion': settingsVersion, GLOBAL.ENABLED: settings.get(GLOBAL.ENABLED, True) and not warning,
            'showToggleButton': GLOBAL.ENABLED in settings and not warning, 'inBattle': False,
            'position': CONFIG_INTERFACE.BLOCK_IDS.index(blockID), 'column1': column1, 'column2': column2
        }

    def createItem(self, blockID, key, value):
        val_type = type(value)
        if isinstance(value, str):
            if GLOBAL.ALIGN in key:
                return self.createRadioButtonGroup(blockID, key,
                                                   *self.getter.getCollectionIndex(value, GLOBAL.ALIGN_LIST))
            if blockID == HP_BARS.NAME and HP_BARS.STYLE == key:
                return self.createRadioButtonGroup(blockID, key,
                                                   *self.getter.getCollectionIndex(value, HP_BARS.STYLES))
        if isinstance(value, (str, bool)):
            return self.createControl(blockID, key, value)
        elif val_type is int:
            if DISPERSION.CIRCLE_SCALE_CONFIG in key:
                return self.createSlider(blockID, key, GLOBAL.ONE, 100, GLOBAL.ONE, value)
            return self.createStepper(blockID, key, -2000, 2000, GLOBAL.ONE, value)
        elif val_type is float:
            if STATISTICS.ICON_BLACKOUT in key:
                return self.createStepper(blockID, key, -2.0, 2.0, 0.01, value)
            if GLOBAL.ZERO <= value <= GLOBAL.F_ONE:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 2.0, 0.01, value)
            else:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 300.0, GLOBAL.F_ONE, value)
        elif val_type is list:
            if "_hotkey" in key:
                return self.createHotKey(blockID, key, value, KEY_ALT)
            if SNIPER.STEPS in key:
                return self.createControl(blockID, key, GLOBAL.COMMA_SEP.join((str(x) for x in value)))


class Getter(object):
    __slots__ = ()

    @staticmethod
    def getLinkToParam(data, settingPath):
        path = settingPath.split(GLOBAL.C_INTERFACE_SPLITTER)
        for fragment in path:
            if fragment in data and isinstance(data[fragment], dict):
                data = data[fragment]
        return data, path[GLOBAL.LAST]

    @staticmethod
    def getCollectionIndex(value, collection):
        index = GLOBAL.ZERO
        if value in collection:
            index = collection.index(value)
        return collection, index

    def getKeyPath(self, settings, path=()):
        for key, value in settings.iteritems():
            key_path = path + (key,)
            if isinstance(value, dict):
                for _path in self.getKeyPath(value, key_path):
                    yield _path
            else:
                yield key_path

    def keyValueGetter(self, settings):
        key_val = []
        try:
            for key in sorted(self.getKeyPath(settings)):
                key = GLOBAL.C_INTERFACE_SPLITTER.join(key)
                if GLOBAL.ENABLED != key:
                    dic, param = self.getLinkToParam(settings, key)
                    key_val.append((key, dic[param]))
        except Exception:
            LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
        return key_val


class ConfigInterface(CreateElement):

    def __init__(self, modsListApi, vxSettingsApi, vxSettingsApiEvents, settings, configLoader):
        super(ConfigInterface, self).__init__()
        self.cLoader = configLoader
        self.modsListApi = modsListApi
        self.settings = settings
        self.apiEvents = vxSettingsApiEvents
        self.inited = set()
        self.vxSettingsApi = vxSettingsApi
        self.currentConfig = self.newConfig = self.cLoader.configsList.index(self.cLoader.cName)
        self.newConfigLoadingInProcess = self.currentConfig != self.newConfig
        self.getter = Getter()
        vxSettingsApi.addContainer(MOD_NAME, localization['service'], skipDiskCache=True,
                                   useKeyPairs=self.settings.main[MAIN.USE_KEY_PAIRS])
        vxSettingsApi.onFeedbackReceived += self.onFeedbackReceived
        ServicesLocator.appLoader.onGUISpaceEntered += self.loadHangarSettings
        self.settings.onUserConfigUpdateComplete += self.onUserConfigUpdateComplete

    def loadHangarSettings(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOGIN:
            self.addModificationToModList()
            self.addModsToVX()
            ServicesLocator.appLoader.onGUISpaceEntered -= self.loadHangarSettings

    def addModificationToModList(self):
        """register settings_core window in modsListApi"""
        kwargs = {
            'id': MOD_NAME, 'name': localization['service']['name'],
            'description': localization['service']['description'],
            'icon': 'gui/maps/icons/battle_observer/hangar_settings_image.png',
            GLOBAL.ENABLED: True, 'login': True, 'lobby': True, 'callback': self.load_window
        }
        self.modsListApi.addModification(**kwargs)

    def addModsToVX(self):
        for blockID in CONFIG_INTERFACE.BLOCK_IDS:
            if blockID in self.inited:
                continue
            try:
                self.vxSettingsApi.addMod(MOD_NAME, blockID, lambda *args: self.getTemplate(blockID),
                                          dict(), lambda *args: None, button_handler=self.onButtonPress)
            except Exception as err:
                logWarning('ConfigInterface startLoad {}'.format(repr(err)))
                LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
            else:
                self.inited.add(blockID)

    def load_window(self):
        """Loading settings_core window"""
        self.vxSettingsApi.loadWindow(MOD_NAME)

    def onUserConfigUpdateComplete(self):
        if self.newConfigLoadingInProcess:
            for blockID in CONFIG_INTERFACE.BLOCK_IDS:
                self.updateMod(blockID)
            self.load_window()

    def onFeedbackReceived(self, container, event):
        """Feedback EVENT"""
        if container != MOD_NAME:
            return
        self.newConfigLoadingInProcess = self.currentConfig != self.newConfig
        if event == self.apiEvents.WINDOW_CLOSED:
            self.vxSettingsApi.onSettingsChanged -= self.onSettingsChanged
            self.vxSettingsApi.onDataChanged -= self.onDataChanged
            if self.newConfigLoadingInProcess:
                self.inited.clear()
                self.cLoader.readConfig(self.cLoader.configsList[self.newConfig])
                self.cLoader.createLoadJSON(cName=self.cLoader.configsList[self.newConfig])
                self.currentConfig = self.newConfig
        elif event == self.apiEvents.WINDOW_LOADED:
            self.vxSettingsApi.onSettingsChanged += self.onSettingsChanged
            self.vxSettingsApi.onDataChanged += self.onDataChanged

    def updateMod(self, blockID):
        if blockID not in self.inited:
            try:
                self.vxSettingsApi.updateMod(MOD_NAME, blockID, lambda *args: self.getTemplate(blockID))
                self.inited.add(blockID)
            except Exception:
                LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])

    def onSettingsChanged(self, modID, blockID, data):
        """Saves made by the user settings_core in the settings_core file."""
        if self.newConfigLoadingInProcess or MOD_NAME != modID:
            return
        if blockID == ANOTHER.CONFIG_SELECT and self.currentConfig != data['selector']:
            self.newConfig = data['selector']
            self.vxSettingsApi.processEvent(MOD_NAME, self.apiEvents.CALLBACKS.CLOSE_WINDOW)
            if self.settings.main[MAIN.DEBUG]:
                logInfo("change settings '%s' - %s" % (self.cLoader.configsList[self.newConfig], blockID))
        else:
            settings = getattr(self.settings, blockID)
            for key, value in data.iteritems():
                updatedConfigLink, paramName = self.getter.getLinkToParam(settings, key)
                if paramName in updatedConfigLink:
                    if GLOBAL.ALIGN in key:
                        value = GLOBAL.ALIGN_LIST[value]
                    elif key == HP_BARS.STYLE and not isinstance(value, str):
                        value = HP_BARS.STYLES[value]
                    elif key == "zoomSteps*steps":
                        value = [round(float(x.strip()), GLOBAL.ONE) for x in value.split(',')]
                    newParamType = type(value)
                    oldParamType = type(updatedConfigLink[paramName])
                    if oldParamType != newParamType:
                        if oldParamType is float and newParamType is int:
                            value = float(value)
                        elif oldParamType is int and newParamType is float:
                            value = int(round(value))
                    updatedConfigLink[paramName] = value
            self.cLoader.updateConfigFile(blockID, settings)
            self.settings.onModSettingsChanged(settings, blockID)

    def onDataChanged(self, modID, blockID, varName, value, *a, **k):
        """Darkens dependent elements..."""
        if modID != MOD_NAME or blockID not in CONFIG_INTERFACE.BLOCK_IDS:
            return
        if blockID in CONFIG_INTERFACE.HANDLER_VALUES:
            if varName in CONFIG_INTERFACE.HANDLER_VALUES[blockID]:
                values = CONFIG_INTERFACE.HANDLER_VALUES[blockID][varName]
                self.setHandlerValue(blockID, values, value)
        if blockID == MAIN.NAME and varName == MAIN.USE_KEY_PAIRS:
            self.vxSettingsApi.getContainer(MOD_NAME)._vxSettingsCtrl__useHkPairs = value

    def setHandlerValue(self, blockID, values, value):
        getObject = self.vxSettingsApi.getDAAPIObject
        for varName in values:
            obj = getObject(blockID, varName)
            if obj is not None:
                obj.alpha = 0.4 if not value else GLOBAL.F_ONE
                obj.mouseEnabled = value
                obj.mouseChildren = value
                obj.tabEnabled = value

    @staticmethod
    def onButtonPress(container, blockID, varName, value):
        if container == MOD_NAME and blockID == ANOTHER.CONFIG_SELECT:
            if varName in CONFIG_INTERFACE.DONATE_BUTTONS:
                openWebBrowser(value)

    def getTemplate(self, blockID):
        """create templates, do not change..."""
        settings = getattr(self.settings, blockID, {})
        column1 = []
        column2 = []
        if blockID == ANOTHER.CONFIG_SELECT:
            column1 = [self.createRadioButtonGroup(blockID, 'selector', self.cLoader.configsList, self.newConfig)]
            column2 = [self.createControl(blockID, 'donate_button_ua', URLS.DONATE_UA_URL, 'Button'),
                       self.createControl(blockID, 'donate_button_paypal', URLS.PAYPAL_URL, 'Button'),
                       self.createControl(blockID, 'donate_button_patreon', URLS.PATREON_URL, 'Button'),
                       self.createControl(blockID, 'discord_button', URLS.DISCORD, 'Button')]
        else:
            items = []
            for key, value in self.getter.keyValueGetter(settings):
                item = self.createItem(blockID, key, value)
                if item is not None:
                    items.append(item)
            middleIndex = (len(items) + 1) // 2
            for index, item in enumerate(items):
                column = column1 if index < middleIndex else column2
                column.append(item)
        return self.createBlock(blockID, settings, column1, column2)
