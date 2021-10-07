# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen.constants import GLOBAL
from armagomen.utils.common import callback
from armagomen.utils.dialogs import LoadingErrorDialog
from frameworks.wulf import WindowLayer
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader


class LoadingError(object):
    appLoader = dependency.descriptor(IAppLoader)
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self, errorMessage):
        if GLOBAL.RU_LOCALIZATION:
            self.message = "<font size='18'>Ошибка загрузки: файлы <font color='#FFFF00'><b>" \
                           "poliroid.modslistapi*.wotmod | polarfox.vxSettingsApi*.wotmod</b></font> отсутствуют " \
                           "либо повреждены. Пожалуйста скопируйте корректные файлы из архива с модом." \
                           "</font>\n\n{}".format(errorMessage)
        else:
            self.message = "<font size='18'> Error loading: files <font color='#FFFF00'><b>" \
                           "poliroid.modslistapi*.wotmod | polarfox.vxSettingsApi*.wotmod</b></font> missing or " \
                           "damaged. Please copy correct files from the archive with the mod." \
                           "</font>\n\n{}".format(errorMessage)
        self.loadAlias = VIEW_ALIAS.LOGIN if self.getSetting(GAME.LOGIN_SERVER_SELECTION) else VIEW_ALIAS.LOBBY_HANGAR
        self.waitingLoginLoaded()

    def waitingLoginLoaded(self):
        app = self.appLoader.getApp()
        if app is None or app.containerManager is None:
            callback(2.0, self.waitingLoginLoaded)
            return
        view = app.containerManager.getView(WindowLayer.VIEW)
        if view and view.settings.alias == self.loadAlias and view.isCreated():
            dialog = LoadingErrorDialog()
            dialog.setView(view)
            dialog.showLoadingError(self.message)
        else:
            callback(2.0, self.waitingLoginLoaded)
