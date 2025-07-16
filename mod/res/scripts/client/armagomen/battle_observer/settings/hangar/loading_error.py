# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer.i18n.dialogs import error_template
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class LoadingError(object):
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self, errorMessage):
        self.message = error_template.format(errorMessage)
        ServicesLocator.appLoader.onGUISpaceEntered += self.__show

    def __show(self, spaceID):
        in_login = self.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == (GuiGlobalSpaceID.LOGIN if in_login else GuiGlobalSpaceID.LOBBY):
            LoadingErrorDialog().showLoadingError(self.message, GuiGlobalSpaceID.LOBBY == spaceID)
            ServicesLocator.appLoader.onGUISpaceEntered -= self.__show
