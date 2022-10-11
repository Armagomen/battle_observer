# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.app_loader import sf_lobby
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import g_eventBus
from gui.shared.events import AppLifeCycleEvent
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage


class LoadingError(object):
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self, errorMessage):
        self.isDisplayed = False
        language = getClientLanguage()
        if language == 'uk':
            self.message = "<font size='18'>Помилка завантаження: залежності модифікації <font color='#FFFF00'><b>" \
                           "poliroid.modslistapi_*.wotmod та/або polarfox.vxSettingsApi_*.wotmod</b></font> " \
                           "відсутні або пошкоджені.\nБудь ласка, скопіюйте коректні файли із архіву з модифікацією." \
                           "</font>\n\nПовідомлення про помилку: {}".format(errorMessage)
        elif language in ('ru', 'be'):
            self.message = "<font size='18'>Ошибка загрузки: зависимости мода <font color='#FFFF00'><b>" \
                           "poliroid.modslistapi_*.wotmod и/или polarfox.vxSettingsApi_*.wotmod</b></font> " \
                           "отсутствуют либо повреждены.\nПожалуйста скопируйте корректные файлы из архива с модом." \
                           "</font>\n\nСообщение об ошибке: {}".format(errorMessage)
        else:
            self.message = "<font size='18'> Error loading: mod dependencies <font color='#FFFF00'><b>" \
                           "poliroid.modslistapi_*.wotmod and/or polarfox.vxSettingsApi_*.wotmod</b></font> are " \
                           "missing or damaged.\nPlease copy correct files from the mod archive." \
                           "</font>\n\nError message: {}".format(errorMessage)
        self.loadAlias = VIEW_ALIAS.LOGIN if self.getSetting(GAME.LOGIN_SERVER_SELECTION) else VIEW_ALIAS.LOBBY_HANGAR
        g_eventBus.addListener(AppLifeCycleEvent.INITIALIZED, self.__onAppInitialized)

    @sf_lobby
    def app(self):
        pass

    def __onAppInitialized(self, event):
        if event.ns == APP_NAME_SPACE.SF_LOBBY:
            self.app.loaderManager.onViewLoaded += self.__onViewLoaded

    def __onViewLoaded(self, view, *args):
        alias = view.alias
        if alias == self.loadAlias:
            self.__show(view)
            self.__removeListeners()

    def __removeListeners(self):
        if self.app and self.app.loaderManager:
            self.app.loaderManager.onViewLoaded -= self.__onViewLoaded
        g_eventBus.removeListener(AppLifeCycleEvent.INITIALIZED, self.__onAppInitialized)

    def __show(self, view):
        if not self.isDisplayed:
            dialog = LoadingErrorDialog()
            dialog.setView(view)
            dialog.showLoadingError(self.message)
            self.isDisplayed = True
