from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import getRandomBigLogo
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

    @async
    def showUpdateError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(getRandomBigLogo() + "\nERROR DOWNLOAD UPDATE")
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel="CLOSE")
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)

    @async
    def showUpdateFinished(self, title, message, buttons):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=buttons['restart'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons['cancel'])
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self, title, message, urls, buttons):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=buttons['auto'])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons['handle'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons['cancel'])
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            openWebBrowser(urls['full'])
        raise AsyncReturn(result.result == DialogButtons.RESEARCH)


class LoadingErrorDialog(DialogBase):

    @async
    def showLoadingError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(getRandomBigLogo())
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
        builder.setFormattedTitle(getRandomBigLogo() + "\n" + vehicle_name)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.SUBMIT, None, True, rawLabel=self.localized["submit"])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localized["cancel"])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=self.localized["ignore"])
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            addVehicleToCache(vehicle_name)
        raise AsyncReturn(result.result == DialogButtons.SUBMIT)
