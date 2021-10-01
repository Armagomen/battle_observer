import os
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from Event import SafeEvent
from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer import __version__
from armagomen.constants import GLOBAL, URLS, MESSAGES
from armagomen.utils.common import logInfo, logError, getCurrentModPath, callback, \
    urlResponse
from armagomen.utils.events import g_events
from armagomen.utils.dialogs import UpdateDialogs
from frameworks.wulf import WindowLayer
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from web.cache.web_downloader import WebDownloader


class DownloadThread(object):
    __slots__ = ("dialog", "onDownloadFinished")

    def __init__(self, dialog):
        self.dialog = dialog
        self.onDownloadFinished = SafeEvent()

    def start(self, url, info):
        Waiting.show('updating')
        downloader = WebDownloader(GLOBAL.ONE)
        try:
            logInfo('downloading started {} at {}'.format(info, url))
            downloader.download(url, self.onDownloaded)
        except Exception as error:
            message = 'update {} - download failed: {}'.format(info, repr(error))
            Waiting.hide('updating')
            logError(message)
            self.dialog.showUpdateError(message)
        finally:
            downloader.close()

    def onDownloaded(self, _url, data):
        Waiting.hide('updating')
        self.onDownloadFinished(data)
        logInfo('downloading finished: {}'.format(_url))


class UpdateMain(object):
    URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}
    appLoader = dependency.descriptor(IAppLoader)

    __slots__ = ("inLogin", "view", "dialogs", "download", "workingDir", "updateData")

    def __init__(self):
        self.inLogin = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.view = None
        self.workingDir = os.path.join(*getCurrentModPath())
        self.dialogs = UpdateDialogs()
        self.download = DownloadThread(self.dialogs)
        self.updateData = defaultdict()

        self.dialogs.onClickDownload += self.onDownloadStart
        self.download.onDownloadFinished += self.onDownloadFinished

    def onDownloadStart(self):
        info = self.updateData.get('tag_name', __version__)
        self.download.start(self.URLS['last'], info)

    def onDownloadFinished(self, data):
        if data is not None:
            old_files = os.listdir(self.workingDir)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, self.workingDir)
        self.dialogs.showUpdateFinished(self.updateData)

    def request_last_version(self):
        result = False
        params = urlResponse(URLS.UPDATE_GITHUB_API_URL)
        if params:
            self.updateData.update(params)
            new_version = params.get('tag_name', __version__)
            local_ver = self.tupleVersion(__version__)
            server_ver = self.tupleVersion(new_version)
            if local_ver < server_ver:
                assets = params.get('assets')
                for asset in assets:
                    filename = asset.get('name', '')
                    download_url = asset.get('browser_download_url')
                    if filename == 'AutoUpdate.zip':
                        self.URLS['last'] = download_url
                    elif filename.startswith('BattleObserver_'):
                        self.URLS['full'] = download_url
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
        else:
            self.dialogs = None
            self.download = None

    def waitingLoginLoaded(self):
        app = self.appLoader.getApp()
        if app is None or app.containerManager is None:
            callback(2.0, self.waitingLoginLoaded)
            return
        view = app.containerManager.getView(WindowLayer.VIEW)
        if view and view.settings.alias == VIEW_ALIAS.LOGIN and view.isCreated():
            self.dialogs.setView(view)
            self.dialogs.showNewVersionAvailable(self.updateData, self.workingDir, self.URLS)
        else:
            callback(2.0, self.waitingLoginLoaded)

    def onHangarLoaded(self, view):
        self.dialogs.setView(view)
        self.dialogs.showNewVersionAvailable(self.updateData, self.workingDir, self.URLS)
        g_events.onHangarLoaded -= self.onHangarLoaded
