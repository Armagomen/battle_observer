# coding=utf-8
from collections import namedtuple

from armagomen._constants import getLogo, GLOBAL
from armagomen.battle_observer.i18n.dialogs import ban_info, labels
from armagomen.utils.common import closeClient, disconnect, openWebBrowser
from frameworks.wulf import WindowLayer
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import InfoDialogBuilder, WarningDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework.entities.View import ViewKey
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from wg_async import AsyncReturn, wg_async, wg_await

buttons = namedtuple("BUTTONS", "close_game auto handle cancel close apply ignore yes no")(*labels)


class DialogBase(object):
    appLoader = dependency.descriptor(IAppLoader)

    @property
    def view(self):
        app = self.appLoader.getApp()
        if app is None or app.containerManager is None:
            return None
        view = app.containerManager.getView(WindowLayer.VIEW)
        if view is None:
            view = app.containerManager.getViewByKey(ViewKey(VIEW_ALIAS.LOGIN))
        return view


class BannedDialog(DialogBase):

    @wg_async
    def showDialog(self, databaseId, name):
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(getLogo())
        builder.setFormattedMessage(ban_info.format(databaseId, name))
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel=buttons.close)
        result = yield wg_await(dialogs.show(builder.buildInLobby()))
        if result.result == DialogButtons.CANCEL:
            disconnect()
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
