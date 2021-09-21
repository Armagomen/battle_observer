import json
import os
import re
import urllib2
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from gui.Scaleform.Waiting import Waiting
from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer import __version__
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import GLOBAL, URLS, MESSAGES, HEADERS
from armagomen.utils.common import restartGame, logInfo, openWebBrowser, logError, logWarning, \
    getCurrentModPath, callback
from armagomen.utils.events import g_events
from async import async, await, AsyncReturn
from frameworks.wulf import WindowLayer
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import InfoDialogBuilder, WarningDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from web.cache.web_downloader import WebDownloader

LAST_UPDATE = defaultdict()
DOWNLOAD_URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}

workingDir = os.path.join(*getCurrentModPath())


class DialogWindow(object):
    __slots__ = ("localization", "parent")

    def __init__(self, view):
        self.localization = localization['updateDialog']
        self.parent = view

    @async
    def showUpdateError(self, message):
        builder = WarningDialogBuilder()
        builder.setFormattedTitle("ERROR DOWNLOAD - Battle Observer Update")
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.CANCEL, None, True, rawLabel="CLOSE")
        result = yield await(dialogs.showSimple(builder.build(self.parent), DialogButtons.PURCHASE))
        raise AsyncReturn(result)

    @async
    def showUpdateFinished(self):
        message = self.localization['messageOK'].format(LAST_UPDATE.get('tag_name', __version__))
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(self.localization['titleOK'])
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, None, True, rawLabel=self.localization['buttonOK'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localization['buttonCancel'])
        result = yield await(dialogs.showSimple(builder.build(self.parent), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self):
        message = self.localization['messageNEW'].format(workingDir)
        gitMessage = LAST_UPDATE.get("body", GLOBAL.EMPTY_LINE)
        message += '\n\n{0}'.format(re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, gitMessage))
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(self.localization['titleNEW'].format(LAST_UPDATE.get('tag_name', __version__)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, None, True, rawLabel=self.localization['buttonAUTO'])
        builder.addButton(DialogButtons.PURCHASE, None, False, rawLabel=self.localization['buttonHANDLE'])
        builder.addButton(DialogButtons.CANCEL, None, False, rawLabel=self.localization['buttonCancel'])
        result = yield await(dialogs.show(builder.build(self.parent)))
        if result.result == DialogButtons.RESEARCH:
            runDownload = DownloadThread(self)
            runDownload.start()
            Waiting.show('updating')
            raise AsyncReturn(True)
        elif result.result == DialogButtons.PURCHASE:
            openWebBrowser(DOWNLOAD_URLS['full'])
            raise AsyncReturn(True)
        else:
            raise AsyncReturn(False)


class DownloadThread(object):
    __slots__ = ("downloader", "dialog")

    def __init__(self, dialog):
        self.downloader = WebDownloader(GLOBAL.ONE)
        self.dialog = dialog

    def start(self):
        try:
            logInfo('start downloading update {}'.format(LAST_UPDATE.get('tag_name', __version__)))
            self.downloader.download(DOWNLOAD_URLS['last'], self.onDownloaded)
        except Exception as error:
            message = 'update {} - download failed: {}'.format(LAST_UPDATE.get('tag_name', __version__), repr(error))
            Waiting.hide('updating')
            logError(message)
            self.dialog.showUpdateError(message)
        finally:
            self.downloader.close()
            self.downloader = None

    def onDownloaded(self, _url, data):
        if data is not None:
            old_files = os.listdir(workingDir)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, workingDir)
            Waiting.hide('updating')
            self.dialog.showUpdateFinished()
            logInfo('update downloading finished {}'.format(LAST_UPDATE.get('tag_name', __version__)))
        self.dialog = None


class UpdateMain(object):
    appLoader = dependency.descriptor(IAppLoader)
    __slots__ = ("inLogin",)

    def __init__(self):
        self.inLogin = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)

    def get_update_data(self):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
            opener.addheaders = HEADERS
            response = opener.open(URLS.UPDATE_GITHUB_API_URL)
        except urllib2.URLError:
            logWarning("Technical problems with the server, please inform the developer.")
        else:
            return json.load(response)

    def request_last_version(self):
        result = False
        params = self.get_update_data()
        if params:
            LAST_UPDATE.update(params)
            new_version = LAST_UPDATE.get('tag_name', __version__)
            local_ver = self.tupleVersion(__version__)
            server_ver = self.tupleVersion(new_version)
            if local_ver < server_ver:
                assets = LAST_UPDATE.get('assets')
                for asset in assets:
                    filename = asset.get('name', '')
                    download_url = asset.get('browser_download_url')
                    if filename == 'AutoUpdate.zip':
                        DOWNLOAD_URLS['last'] = download_url
                    elif filename.startswith('BattleObserver_'):
                        DOWNLOAD_URLS['full'] = download_url
                result = True
                logInfo(MESSAGES.NEW_VERSION.format(new_version))
            else:
                logInfo(MESSAGES.UPDATE_CHECKED)
        return result

    @staticmethod
    def tupleVersion(version):
        return tuple(map(int, version.split(GLOBAL.DOT)))

    def subscribe(self):
        result = self.request_last_version()
        if result:
            if self.inLogin:
                self.waitingLoginLoaded()
            else:
                g_events.onHangarLoaded += self.onHangarLoaded

    def waitingLoginLoaded(self):
        app = self.appLoader.getApp()
        if app is None or app.containerManager is None:
            callback(2.0, self.waitingLoginLoaded)
            return
        view = app.containerManager.getView(WindowLayer.VIEW)
        if view and view.settings.alias == VIEW_ALIAS.LOGIN and view.isCreated():
            dialog = DialogWindow(view)
            dialog.showNewVersionAvailable()
        else:
            callback(2.0, self.waitingLoginLoaded)

    def onHangarLoaded(self, view):
        dialog = DialogWindow(view)
        dialog.showNewVersionAvailable()
        g_events.onHangarLoaded -= self.onHangarLoaded
