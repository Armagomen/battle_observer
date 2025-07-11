# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from skeletons.gui.app_loader import GuiGlobalSpaceID


class LoadingError(object):
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self, errorMessage):
        if getClientLanguage().lower() in ("uk", "be"):
            self.message = "Повідомлення про помилку: {}".format(errorMessage)
        else:
            self.message = "Error message: {}".format(errorMessage)
        ServicesLocator.appLoader.onGUISpaceEntered += self.__show

    def __show(self, spaceID):
        in_login = self.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == (GuiGlobalSpaceID.LOGIN if in_login else GuiGlobalSpaceID.LOBBY):
            isLobby = GuiGlobalSpaceID.LOBBY == spaceID
            LoadingErrorDialog().showLoadingError(self.message, isLobby)
            ServicesLocator.appLoader.onGUISpaceEntered -= self.__show
