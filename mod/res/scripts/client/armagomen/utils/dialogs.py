# coding=utf-8
from collections import namedtuple

from armagomen.constants import GLOBAL
from armagomen.constants import getRandomBigLogo
from armagomen.utils.common import restartGame, openWebBrowser, addVehicleToCache
from async import async, await, AsyncReturn
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import WarningDialogBuilder, InfoDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons

if GLOBAL.RU_LOCALIZATION:
    labels = ("ПЕРЕЗАГРУЗКА", "Автоматически", "Вручную", "Отмена", "Закрыть", "Применить", "Игнорировать этот танк")
else:
    labels = ("RESTART", "Automatically", "Manually", "Cancel", "Close", "Apply", "Ignore this tank")
buttons = namedtuple("BUTTONS", "restart auto handle cancel close apply ignore")(*labels)


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
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)

    @async
    def showUpdateFinished(self, title, message):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=buttons.restart)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self, title, message, handleURL):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=buttons.auto)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.handle)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            openWebBrowser(handleURL)
        raise AsyncReturn(result.result == DialogButtons.RESEARCH)


class LoadingErrorDialog(DialogBase):

    @async
    def showLoadingError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(getRandomBigLogo())
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)


class CrewDialog(DialogBase):

    @async
    def showCrewDialog(self, title, message, vehicle_name):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.SUBMIT, None, True, rawLabel=buttons.apply)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.ignore)
        result = yield await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            addVehicleToCache(vehicle_name)
        raise AsyncReturn(result.result == DialogButtons.SUBMIT)
