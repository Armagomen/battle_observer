import os
import re
from collections import defaultdict
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer.core.update.i18n import getI18n
from armagomen.constants import GLOBAL, URLS, MESSAGES, getRandomLogo
from armagomen.utils.common import logInfo, logError, getCurrentModPath, urlResponse, getUpdatePath
from armagomen.utils.dialogs import UpdateDialogs
from armagomen.utils.events import g_events
from async import async, await
from gui.Scaleform.Waiting import Waiting
from gui.shared.personality import ServicesLocator
from web.cache.web_downloader import WebDownloader

WAITING_UPDATE = 'updating'


class DownloadThread(object):
    URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}
    __slots__ = ("dialogs", "downloader", "updateData", "inLogin", "modPath", "updateData", "i18n", "version")

    def __init__(self):
        self.i18n = getI18n()
        self.updateData = defaultdict()
        self.dialogs = UpdateDialogs()
        self.downloader = None
        self.modPath = os.path.join(*getCurrentModPath())

    def startDownload(self):
        Waiting.show(WAITING_UPDATE)
        mod_version = self.updateData.get('tag_name', self.version)
        path = os.path.join(getUpdatePath(), mod_version + ".zip")
        if os.path.isfile(path):
            logInfo('update is already downloaded to {}'.format(path))
            self.extractZipArchive(path)
            self.dialogs.showUpdateFinished(getRandomLogo() + self.i18n['titleOK'],
                                            self.i18n['messageOK'].format(mod_version))
        else:
            url = self.URLS['last']
            self.downloader = WebDownloader(GLOBAL.ONE)
            if url:
                logInfo('downloading update started {} at {}'.format(mod_version, url))
                self.downloader.download(url, self.onDownloaded)
            else:
                self.closeDownloader()
                self.downloadError(url)

    def closeDownloader(self):
        if self.downloader is not None:
            self.downloader.close()
            self.downloader = None

    def extractZipArchive(self, path):
        old_files = os.listdir(self.modPath)
        with ZipFile(path, "r") as archive:
            for newFile in archive.namelist():
                if newFile not in old_files:
                    logInfo('update, add new file {}'.format(newFile))
                    archive.extract(newFile, self.modPath)
        if Waiting.isOpened(WAITING_UPDATE):
            Waiting.hide(WAITING_UPDATE)

    def onDownloaded(self, _url, data):
        self.closeDownloader()
        if data is not None:
            mod_version = self.updateData.get('tag_name', self.version)
            path = os.path.join(getUpdatePath(), mod_version + ".zip")
            with open(path, "wb") as zipArchive:
                zipArchive.write(data)
            logInfo('downloading update finished to: {}'.format(path))
            self.extractZipArchive(path)
            self.dialogs.showUpdateFinished(getRandomLogo() + self.i18n['titleOK'],
                                            self.i18n['messageOK'].format(mod_version))
        else:
            self.downloadError(_url)

    def downloadError(self, url):
        if Waiting.isOpened(WAITING_UPDATE):
            Waiting.hide(WAITING_UPDATE)
        message = 'update download failed: {}'.format(url)
        logError(message)
        self.dialogs.showUpdateError(message)


class UpdateMain(DownloadThread):
    __slots__ = ("dialogs", "downloader", "updateData", "inLogin", "modPath", "updateData", "i18n", "version")

    def __init__(self, version):
        super(UpdateMain, self).__init__()
        self.version = version
        self.inLogin = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.subscribe()

    def request_last_version(self):
        result = False
        params = urlResponse(URLS.UPDATE_GITHUB_API_URL)
        if params:
            self.updateData.update(params)
            new_version = params.get('tag_name', self.version)
            local_ver = self.tupleVersion(self.version)
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
                g_events.onLoginLoaded += self.showDialog
            else:
                g_events.onHangarLoaded += self.showDialog
        else:
            self.dialogs = None

    @async
    def showDialog(self, view):
        self.dialogs.setView(view)
        title = getRandomLogo() + self.i18n['titleNEW'].format(self.updateData.get('tag_name', self.version))
        gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get("body", GLOBAL.EMPTY_LINE))
        message = self.i18n['messageNEW'].format(self.modPath, gitMessage)
        result = yield await(self.dialogs.showNewVersionAvailable(title, message, self.URLS['full']))
        if result:
            self.startDownload()
        if self.inLogin:
            g_events.onLoginLoaded -= self.showDialog
        else:
            g_events.onHangarLoaded -= self.showDialog
