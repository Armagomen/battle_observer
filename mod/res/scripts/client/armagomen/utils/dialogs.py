# coding=utf-8
from collections import namedtuple

from armagomen._constants import getLogo, GLOBAL
from armagomen.utils.common import closeClient, openWebBrowser
from armagomen.utils.logging import logInfo
from frameworks.wulf import WindowLayer
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import InfoDialogBuilder, WarningDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from helpers import dependency, getClientLanguage
from skeletons.gui.app_loader import IAppLoader
from wg_async import AsyncReturn, wg_async, wg_await

language = getClientLanguage().lower()
if language == "uk":
    labels = ("Закрити гру", "Автоматично", "Вручну", "Скасувати", "Закрити", "Застосувати",
              "Ігнорувати цей танк", "Так", "Ні")
    ban_info = ('Доступ заборонено\n\nID: {}\nІм`я: {}\n\nВаш доступ до цієї послуги обмежено.Якщо ви вважаєте, що це помилка, або хочете '
                'оскаржити рішення, зверніться до служби підтримки, вказавши свій ідентифікатор користувача.\n\nДякуємо за розуміння.')
elif language in ('ru', 'be'):
    labels = ("Закрыть игру", "Автоматически", "Ручной режим", "Отменить", "Закрыть", "Применить",
              "Игнорировать танк", "Да", "Нет")
    ban_info = ('Доступ запрещён\n\nID: {}\nИмя: {}\n\nВаш доступ к этой услуге ограничен. Если вы считаете, что это ошибка, или хотите '
                'обжаловать решение, обратитесь в службу поддержки, указав свой идентификатор пользователя.\n\nБлагодарим за понимание.')
else:
    labels = ("Close game", "Automatically", "Manually", "Cancel", "Close", "Apply", "Ignore this tank", "Yes", "No")
    ban_info = ('Access Denied\n\nID: {}\nName: {}\n\nYour access to this service has been restricted. If you believe this is a mistake or '
                'would like to appeal the decision, please contact support with your User ID.\n\nThank you for your understanding.')
buttons = namedtuple("BUTTONS", "close_game auto handle cancel close apply ignore yes no")(*labels)


class DialogBase(object):
    appLoader = dependency.descriptor(IAppLoader)

    @property
    def view(self):
        app = self.appLoader.getApp()
        if app is not None and app.containerManager is not None:
            return app.containerManager.getView(WindowLayer.VIEW)
        return None


class BannedDialog(DialogBase):

    @wg_async
    def showDialog(self, databaseId, name):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(getLogo())
        builder.setFormattedMessage(ban_info.format(databaseId, name))
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.show(builder.buildInLobby()))
        logInfo(result)
        if result.result == DialogButtons.CANCEL:
            closeClient()
        raise AsyncReturn(result)


class UpdaterDialogs(DialogBase):

    @wg_async
    def showNewVersionAvailable(self, title, message, handleURL, isLobby):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), title)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=buttons.auto)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.handle)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield wg_await(dialogs.show(builder.buildInLobby() if isLobby else builder.build(self.view)))
        if result.result == DialogButtons.PURCHASE:
            openWebBrowser(handleURL)
        raise AsyncReturn(result.result == DialogButtons.RESEARCH)

    @wg_async
    def showUpdateError(self, message, isLobby):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), "ERROR DOWNLOAD UPDATE")))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.showSimple(builder.buildInLobby() if isLobby else builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)

    @wg_async
    def showUpdateFinished(self, title, message, isLobby):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), title)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=buttons.close_game)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        result = yield wg_await(dialogs.showSimple(builder.buildInLobby() if isLobby else builder.build(self.view), DialogButtons.PURCHASE))
        if result:
            closeClient()
        raise AsyncReturn(result)


class LoadingErrorDialog(DialogBase):

    @wg_async
    def showLoadingError(self, message, isLobby):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(getLogo())
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.showSimple(builder.buildInLobby() if isLobby else builder.build(self.view), DialogButtons.CANCEL))
        raise AsyncReturn(result)


class CrewDialog(DialogBase):

    @wg_async
    def showCrewDialog(self, vehicle_name, message):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), vehicle_name)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.SUBMIT, None, True, rawLabel=buttons.apply)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.cancel)
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=buttons.ignore)
        result = yield wg_await(dialogs.show(builder.buildInLobby()))
        raise AsyncReturn(result)


class ExcludedMapsDialog(DialogBase):

    @wg_async
    def showExcludedMapsDialog(self, header, message):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(GLOBAL.NEW_LINE.join((getLogo(), header)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=buttons.yes)
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=buttons.no)
        result = yield wg_await(dialogs.show(builder.buildInLobby()))
        raise AsyncReturn(result)
