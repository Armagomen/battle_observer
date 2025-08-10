# coding=utf-8
from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL
from armagomen.battle_observer.i18n.dialogs import error_template
from armagomen.utils.common import addCallback
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class LoadingError(object):
    getSetting = ServicesLocator.settingsCore.getSetting

    def __init__(self):
        self.messages = set()
        ServicesLocator.appLoader.onGUISpaceEntered += self.__show

    def __show(self, spaceID):
        if self.messages:
            in_login = self.getSetting(GAME.LOGIN_SERVER_SELECTION)
            if spaceID == (GuiGlobalSpaceID.LOGIN if in_login else GuiGlobalSpaceID.LOBBY):
                addCallback(1.0, self.showDialog, spaceID == GuiGlobalSpaceID.LOBBY)
                ServicesLocator.appLoader.onGUISpaceEntered -= self.__show
        else:
            ServicesLocator.appLoader.onGUISpaceEntered -= self.__show

    def showDialog(self, isLobby):
        LoadingErrorDialog().showLoadingError(GLOBAL.NEW_LINE.join(error_template.format(message) for message in self.messages), isLobby)
        self.messages.clear()
