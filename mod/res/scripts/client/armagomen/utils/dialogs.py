import re

from armagomen.battle_observer import __version__
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import GLOBAL
from armagomen.utils.common import restartGame, openWebBrowser, addVehicleToCache
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

    def __init__(self):
        super(UpdateDialogs, self).__init__()
        self.localized = localization['updateDialog']

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
        message = self.localized['messageOK'].format(params.get('tag_name', __version__))
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(self.localized['titleOK'])
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=self.localized['buttonOK'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localized['buttonCancel'])
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self, params, path, urls):
        message = self.localized['messageNEW'].format(path)
        gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, params.get("body", GLOBAL.EMPTY_LINE))
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(self.localized['titleNEW'].format(params.get('tag_name', __version__)))
        builder.setFormattedMessage(message + "<p align='left'><font size='15'>" + gitMessage + "</font></p>")
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=self.localized['buttonAUTO'])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=self.localized['buttonHANDLE'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localized['buttonCancel'])
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            openWebBrowser(urls['full'])
        raise AsyncReturn(result.result == DialogButtons.RESEARCH)


class LoadingErrorDialog(DialogBase):

    @async
    def showLoadingError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle("Battle Observer")
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel="CLOSE")
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)


class CrewDialog(DialogBase):

    def __init__(self):
        super(CrewDialog, self).__init__()
        self.localized = localization["crewDialog"]

    @async
    def showCrewDialog(self, value, description, vehicle_name):
        message = self.localized[description] + "\n\n" + self.localized["enable" if value else "disable"]
        builder = InfoDialogBuilder()
        builder.setFormattedTitle("Battle Observer\n" + vehicle_name)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.SUBMIT, None, True, rawLabel=self.localized["submit"])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localized["cancel"])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=self.localized["ignore"])
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            addVehicleToCache(vehicle_name)
        raise AsyncReturn(result.result == DialogButtons.SUBMIT)
