import re

from Event import SafeEvent
from armagomen.battle_observer import __version__
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import GLOBAL
from armagomen.utils.common import restartGame, openWebBrowser
from async import async, await, AsyncReturn
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import WarningDialogBuilder, InfoDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons


class DialogBase(object):
    def __init__(self):
        self.view = None

    def setView(self, view):
        self.view = view


class UpdateDialogs(DialogBase):
    __slots__ = ("localization", "view", "onClickDownload")

    def __init__(self):
        super(UpdateDialogs, self).__init__()
        self.localization = localization['updateDialog']
        self.onClickDownload = SafeEvent()

    @async
    def showUpdateError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle("ERROR DOWNLOAD - Battle Observer Update")
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel="CLOSE")
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)

    @async
    def showUpdateFinished(self, params):
        message = self.localization['messageOK'].format(params.get('tag_name', __version__))
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(self.localization['titleOK'])
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=self.localization['buttonOK'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localization['buttonCancel'])
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self, params, path, urls):
        message = self.localization['messageNEW'].format(path)
        gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, params.get("body", GLOBAL.EMPTY_LINE))
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(self.localization['titleNEW'].format(params.get('tag_name', __version__)))
        builder.setFormattedMessage(message + "<p align='left'><font size='15'>" + gitMessage + "</font></p>")
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=self.localization['buttonAUTO'])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=self.localization['buttonHANDLE'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localization['buttonCancel'])
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.RESEARCH:
            self.onClickDownload()
            raise AsyncReturn(True)
        elif result.result == DialogButtons.PURCHASE:
            openWebBrowser(urls['full'])
            raise AsyncReturn(True)
        else:
            raise AsyncReturn(False)


class LoadingErrorDialog(DialogBase):

    @async
    def showLoadingError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle("Battle Observer")
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel="CLOSE")
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)
