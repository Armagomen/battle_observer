from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL
from armagomen.battle_observer.i18n.dialogs import error_template
from armagomen.utils.common import addCallback
from armagomen.utils.dialogs import LoadingErrorDialog
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class ErrorMessages(object):

    def __init__(self):
        self.messages = set()
        ServicesLocator.appLoader.onGUISpaceEntered += self.__show

    def __show(self, spaceID):
        if not self.messages:
            return
        login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        is_lobby = spaceID == GuiGlobalSpaceID.LOBBY
        if spaceID == GuiGlobalSpaceID.LOGIN and login_server_selection or is_lobby:
            addCallback(1.0, self.showDialog, is_lobby)

    @property
    def _messages(self):
        while self.messages:
            yield error_template.format(self.messages.pop())

    def showDialog(self, isLobby):
        LoadingErrorDialog().showLoadingError(GLOBAL.NEW_LINE.join(self._messages), isLobby)

    def fini(self):
        ServicesLocator.appLoader.onGUISpaceEntered -= self.__show

    def add(self, message):
        self.messages.add(message)
