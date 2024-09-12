from armagomen._constants import (ANOTHER, CONFIG_INTERFACE, DEBUG_PANEL, DISPERSION, GLOBAL, HP_BARS, MAIN, MINIMAP,
                                  MOD_NAME, PANELS, SIXTH_SENSE, SNIPER, STATISTICS, URLS)
from armagomen.battle_observer.settings import user_settings
from armagomen.battle_observer.settings.hangar.i18n import localization, LOCKED_MESSAGE
from armagomen.utils.common import openWebBrowser, xvmInstalled
from armagomen.utils.logging import logError, logInfo, logWarning
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import dependency
from Keys import KEY_LALT, KEY_RALT
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader

settingsVersion = 37
LOCKED_BLOCKS = (STATISTICS.NAME, PANELS.PANELS_NAME, MINIMAP.NAME)


def makeTooltip(header=None, body=None, note=None, attention=None):
    res_str = ''
    if header is not None:
        res_str += '{HEADER}%s{/HEADER}' % header
    if body is not None:
        res_str += '{BODY}%s{/BODY}' % body
    if note is not None:
        res_str += '{NOTE}%s{/NOTE}' % note
    if attention is not None:
        res_str += '{ATTENTION}%s{/ATTENTION}' % attention
    return res_str


def importApi():
    try:
        from gui.modsListApi import g_modsListApi
        from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents
    except Exception as error:
        from armagomen.battle_observer.settings.hangar.loading_error import LoadingError
        from debug_utils import LOG_CURRENT_EXCEPTION
        LoadingError(repr(error))
        LOG_CURRENT_EXCEPTION()
        logError("Settings Api Not Loaded")
    else:
        return g_modsListApi, vxSettingsApi, vxSettingsApiEvents
    return None


class Getter(object):
    __slots__ = ()

    @staticmethod
    def getLinkToParam(settings_block, settingPath):
        path = settingPath.split(GLOBAL.C_INTERFACE_SPLITTER)
        for fragment in path:
            if fragment in settings_block and isinstance(settings_block[fragment], dict):
                settings_block = settings_block[fragment]
        return settings_block, path[GLOBAL.LAST]

    @staticmethod
    def getCollectionIndex(value, collection):
        index = GLOBAL.ZERO
        if value in collection:
            index = collection.index(value)
        return collection, index

    def getKeyPath(self, settings_block, path=()):
        for key, value in settings_block.iteritems():
            key_path = path + (key,)
            if isinstance(value, dict):
                for _path in self.getKeyPath(value, key_path):
                    yield _path
            else:
                yield key_path

    def keyValueGetter(self, settings_block):
        for key in self.getKeyPath(settings_block):
            key = GLOBAL.C_INTERFACE_SPLITTER.join(key)
            if GLOBAL.ENABLED != key:
                dic, param = self.getLinkToParam(settings_block, key)
                yield key, dic[param]


class CreateElement(Getter):

    def __init__(self):
        super(CreateElement, self).__init__()

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
            elif type(value) == bool:
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

    def createDropDown(self, blockID, varName, values, value):
        result = self.createControl(blockID, varName, value, cType='Dropdown')
        if result is not None:
            result.update({'options': [{'label': x} for x in values]})
        return result

    def createSixthSenseDropDown(self, blockID, varName, icons, icon):
        result = self.createControl(blockID, varName, icon, cType='Dropdown')
        if result is not None:
            image = "<img src='img://gui/maps/icons/battle_observer/sixth_sense/{}' width='180' height='180'>"
            result.update({'options': [{'label': x[:-4], 'tooltip': makeTooltip(body=image.format(x))} for x in icons],
                           GLOBAL.WIDTH: 180})
        return result

    def createDebugStyleDropDown(self, blockID, varName, icons, icon):
        result = self.createControl(blockID, varName, icon, cType='Dropdown')
        if result is not None:
            image = "<img src='img://gui/maps/icons/battle_observer/style/debug/{}.jpg' width='240' height='52'>"
            result.update({'options': [{'label': x, 'tooltip': makeTooltip(body=image.format(x))} for x in icons],
                           GLOBAL.WIDTH: 190})
        return result

    def createBarStyleDropDown(self, blockID, varName, icons, icon):
        result = self.createControl(blockID, varName, icon, cType='Dropdown')
        if result is not None:
            image = "<img src='img://gui/maps/icons/battle_observer/style/health/{}.jpg' width='300' height='24'>"
            result.update({'options': [{'label': x, 'tooltip': makeTooltip(body=image.format(x))} for x in icons],
                           GLOBAL.WIDTH: 190})
        return result

    def createRadioButtonGroup(self, blockID, varName, options, value):
        result = self.createDropDown(blockID, varName, options, value)
        if result is not None:
            result.update(type="RadioButtonGroup")
        return result

    def createHotKey(self, blockID, varName, value):
        result = self.createControl(blockID, varName, value, cType='KeyInput')
        if result is not None:
            result['defaultValue'] = [[KEY_LALT, KEY_RALT]]
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

    @staticmethod
    def createBlock(blockID, params, column1, column2):
        name = localization.get(blockID, {}).get("header", blockID)
        warning = xvmInstalled and blockID in LOCKED_BLOCKS
        if warning:
            name = " ".join((name, "<font color='#ff3d3d'>{}</font>".format(LOCKED_MESSAGE)))
        return {
            'modDisplayName': "<font color='#FFFFFF'>{}</font>".format(name),
            'settingsVersion': settingsVersion, GLOBAL.ENABLED: params.get(GLOBAL.ENABLED, True) and not warning,
            'showToggleButton': GLOBAL.ENABLED in params and not warning, 'inBattle': False,
            'position': CONFIG_INTERFACE.BLOCK_IDS.index(blockID), 'column1': column1, 'column2': column2
        }

    def createItem(self, blockID, key, value):
        val_type = type(value)
        if val_type == str:
            if GLOBAL.ALIGN in key:
                return self.createRadioButtonGroup(blockID, key, *self.getCollectionIndex(value, GLOBAL.ALIGN_LIST))
            elif blockID == HP_BARS.NAME and HP_BARS.STYLE == key:
                return self.createBarStyleDropDown(blockID, key, *self.getCollectionIndex(value, HP_BARS.STYLES))
            elif blockID == DEBUG_PANEL.NAME and DEBUG_PANEL.STYLE == key:
                return self.createDebugStyleDropDown(blockID, key, *self.getCollectionIndex(value, DEBUG_PANEL.STYLES))
            elif blockID == SIXTH_SENSE.NAME and key == SIXTH_SENSE.ICON_NAME:
                return self.createSixthSenseDropDown(blockID, key, *self.getCollectionIndex(value, SIXTH_SENSE.ICONS))
        if val_type == str or val_type == bool:
            return self.createControl(blockID, key, value)
        elif val_type == int:
            return self.createStepper(blockID, key, -2000, 2000, GLOBAL.ONE, value)
        elif val_type == float:
            if DISPERSION.SCALE in key:
                return self.createSlider(blockID, key, 0.3, 1.0, 0.01, value)
            if STATISTICS.ICON_BLACKOUT in key:
                return self.createStepper(blockID, key, -2.0, 2.0, 0.01, value)
            elif GLOBAL.ZERO <= value <= GLOBAL.F_ONE:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 2.0, 0.01, value)
            else:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 300.0, GLOBAL.F_ONE, value)
        elif val_type == list:
            if "_hotkey" in key:
                return self.createHotKey(blockID, key, value)
            elif SNIPER.STEPS in key:
                return self.createControl(blockID, key, GLOBAL.COMMA_SEP.join((str(x) for x in value)))


class SettingsInterface(CreateElement):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self, settingsLoader, version):
        api = importApi()
        if api is None:
            return
        self.modsListApi, self.vxSettingsApi, self.apiEvents = api
        super(SettingsInterface, self).__init__()
        self.loader = settingsLoader
        self.inited = set()
        self.currentConfigID = self.newConfigID = self.loader.configsList.index(self.loader.configName)
        self.newConfigLoadingInProcess = False
        user_settings.onUserConfigUpdateComplete += self.onUserConfigUpdateComplete
        localization['service']['name'] = localization['service']['name'].format(version)
        localization['service']['windowTitle'] = localization['service']['windowTitle'].format(version)
        self.appLoader.onGUISpaceEntered += self.addToAPI

    def addToAPI(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOBBY:
            self.addModsToVX()
            self.addModificationToModList()
            self.appLoader.onGUISpaceEntered -= self.addToAPI


    def addModificationToModList(self):
        """register settings window in modsListApi"""
        kwargs = {
            'name': localization['service']['name'], 'description': localization['service']['description'],
            'icon': 'gui/maps/icons/battle_observer/hangar_settings_image.png',
            GLOBAL.ENABLED: True, 'login': False, 'lobby': True, 'callback': self.load_window
        }
        self.modsListApi.addModification(MOD_NAME, **kwargs)

    def addModsToVX(self):
        self.vxSettingsApi.addContainer(MOD_NAME, localization['service'], skipDiskCache=True,
                                        useKeyPairs=user_settings.main[MAIN.USE_KEY_PAIRS])
        for blockID in CONFIG_INTERFACE.BLOCK_IDS:
            if blockID in self.inited:
                continue
            try:
                template = self.getTemplate(blockID)
                if template is not None:
                    self.vxSettingsApi.addMod(MOD_NAME, blockID, lambda *args: template, dict(), lambda *args: None,
                                              button_handler=self.onButtonPress)
            except Exception as err:
                logWarning('SettingsInterface addModsToVX: {}'.format(repr(err)))
                LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
            else:
                self.inited.add(blockID)
        self.vxSettingsApi.onFeedbackReceived += self.onFeedbackReceived

    def load_window(self):
        """Loading settings window"""
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
        self.newConfigLoadingInProcess = self.currentConfigID != self.newConfigID
        if event == self.apiEvents.WINDOW_CLOSED:
            self.vxSettingsApi.onSettingsChanged -= self.onSettingsChanged
            self.vxSettingsApi.onDataChanged -= self.onDataChanged
            if self.newConfigLoadingInProcess:
                self.inited.clear()
                self.loader.readOtherConfig(self.newConfigID)
                self.currentConfigID = self.newConfigID
        elif event == self.apiEvents.WINDOW_LOADED:
            self.vxSettingsApi.onSettingsChanged += self.onSettingsChanged
            self.vxSettingsApi.onDataChanged += self.onDataChanged

    def updateMod(self, blockID):
        if blockID not in self.inited:
            try:
                template = self.getTemplate(blockID)
                if template is not None:
                    self.vxSettingsApi.updateMod(MOD_NAME, blockID, lambda *args: template)
            except Exception:
                LOG_CURRENT_EXCEPTION(tags=[MOD_NAME])
            else:
                self.inited.add(blockID)

    def onSettingsChanged(self, modID, blockID, data):
        """Saves made by the user settings in the settings file."""
        if self.newConfigLoadingInProcess or MOD_NAME != modID:
            return
        if blockID == ANOTHER.CONFIG_SELECT and self.currentConfigID != data['selector']:
            self.newConfigID = data['selector']
            self.vxSettingsApi.processEvent(MOD_NAME, self.apiEvents.CALLBACKS.CLOSE_WINDOW)
            logInfo("change config '{}' - {}", self.loader.configsList[self.newConfigID], blockID)
        else:
            settings_block = getattr(user_settings, blockID, None)
            if settings_block is None:
                return
            for key, value in data.iteritems():
                updated_config_link, param_name = self.getLinkToParam(settings_block, key)
                print param_name, value
                if param_name in updated_config_link:
                    if GLOBAL.ALIGN in key:
                        value = GLOBAL.ALIGN_LIST[value]
                    elif blockID == HP_BARS.NAME and key == HP_BARS.STYLE and not isinstance(value, basestring):
                        value = HP_BARS.STYLES[value]
                    elif blockID == DEBUG_PANEL.NAME and key == DEBUG_PANEL.STYLE and not isinstance(value, basestring):
                        value = DEBUG_PANEL.STYLES[value]
                    elif blockID == SIXTH_SENSE.NAME and key == SIXTH_SENSE.ICON_NAME and not isinstance(value,
                                                                                                         basestring):
                        value = SIXTH_SENSE.ICONS[value]
                    elif blockID == SNIPER.NAME and SNIPER.STEPS == param_name and isinstance(value, basestring):
                        value = value.strip().split(',')
                        if value:
                            value = [val for val in (round(float(x.strip()), GLOBAL.ONE) for x in value) if val >= 2.0]
                        else:
                            value = SNIPER.DEFAULT_STEPS
                    if type(value) == int and type(updated_config_link[param_name]) == float:
                        value = float(value)
                    updated_config_link[param_name] = value
            self.loader.updateConfigFile(blockID, settings_block)
            user_settings.onModSettingsChanged(settings_block, blockID)

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
        get_object = self.vxSettingsApi.getDAAPIObject
        for varName in values:
            obj = get_object(blockID, varName)
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

    def items(self, blockID, settings_block):
        for key, value in self.keyValueGetter(settings_block):
            item = self.createItem(blockID, key, value)
            if item is not None:
                yield item

    def getTemplate(self, blockID):
        """Create templates, do not change..."""
        settings_block = getattr(user_settings, blockID, {})
        if blockID == ANOTHER.CONFIG_SELECT:
            column1 = [self.createRadioButtonGroup(blockID, 'selector', self.loader.configsList, self.currentConfigID)]
            column2 = [self.createControl(blockID, 'donate_button_ua', URLS.MONO, 'Button'),
                       self.createControl(blockID, 'discord_button', URLS.DISCORD, 'Button')]
        else:
            columns = sorted(self.items(blockID, settings_block), key=lambda x: x["varName"])
            middle_index = (len(columns) + int(len(columns) % 2 != 0)) / 2
            column1 = columns[:middle_index]
            column2 = columns[middle_index:]
        return self.createBlock(blockID, settings_block, column1, column2) if column1 or column2 else None
