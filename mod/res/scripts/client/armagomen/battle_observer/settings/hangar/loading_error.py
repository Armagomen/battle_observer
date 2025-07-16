# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from skeletons.gui.app_loader import GuiGlobalSpaceID

lang = getClientLanguage().lower()
error_template = {
    "uk": "Повідомлення про помилку: {}",
    "be": "Паведамленне пра памылку: {}",
    "ru": "Сообщение об ошибке: {}",
    "pl": "Komunikat o błędzie: {}",
    "de": "Fehlermeldung: {}"
}.get(lang, "Error message: {}")


class LoadingError(object):
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self, errorMessage):
        self.message = error_template.format(errorMessage)
        ServicesLocator.appLoader.onGUISpaceEntered += self.__show

    def __show(self, spaceID):
        in_login = self.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == (GuiGlobalSpaceID.LOGIN if in_login else GuiGlobalSpaceID.LOBBY):
            isLobby = GuiGlobalSpaceID.LOBBY == spaceID
            LoadingErrorDialog().showLoadingError(self.message, isLobby)
            ServicesLocator.appLoader.onGUISpaceEntered -= self.__show
