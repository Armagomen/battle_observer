# coding=utf-8
from collections import namedtuple

from armagomen.constants import getLogo, GLOBAL
from armagomen.utils.common import restartGame, openWebBrowser, addVehicleToCache
from frameworks.wulf import WindowLayer
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import WarningDialogBuilder, InfoDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from helpers import getClientLanguage, dependency
from skeletons.gui.app_loader import IAppLoader
from wg_async import wg_async, wg_await, AsyncReturn

language = getClientLanguage()
if language == 'uk':
    labels = ("ПЕРЕЗАВАНТАЖЕННЯ", "Автоматично", "Вручну", "Скасувати", "Закрити", "Застосувати", "Ігнорувати цей танк")
elif language in ('ru', 'be'):
    labels = ("ПЕРЕЗАГРУЗКА", "Автоматически", "Вручную", "Отмена", "Закрыть", "Применить", "Игнорировать этот танк")
else:
    labels = ("RESTART", "Automatically", "Manually", "Cancel", "Close", "Apply", "Ignore this tank")
buttons = namedtuple("BUTTONS", "restart auto handle cancel close apply ignore")(*labels)


class DialogBase(object):
    appLoader = dependency.descriptor(IAppLoader)

    @property
    def view(self):
        app = self.appLoader.getApp()
        if app is not None and app.containerManager is not None:
            return app.containerManager.getView(WindowLayer.VIEW)
        return None


class UpdaterDialogs(DialogBase):

    @wg_async
    def showUpdateError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), "ERROR DOWNLOAD UPDATE")))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)

    @wg_async
    def showUpdateFinished(self, title, message):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=buttons.restart)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield wg_await(dialogs.showSimple(builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @wg_async
    def showNewVersionAvailable(self, title, message, handleURL):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=buttons.auto)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.handle)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield wg_await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            openWebBrowser(handleURL)
        raise AsyncReturn(result.result == DialogButtons.RESEARCH)


class LoadingErrorDialog(DialogBase):

    @wg_async
    def showLoadingError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(getLogo())
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.showSimple(builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)


class CrewDialog(DialogBase):

    @wg_async
    def showCrewDialog(self, title, message, vehicle_name):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(title)
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.SUBMIT, None, True, rawLabel=buttons.apply)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.ignore)
        result = yield wg_await(dialogs.show(builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            addVehicleToCache(vehicle_name)
        raise AsyncReturn(result.result == DialogButtons.SUBMIT)
