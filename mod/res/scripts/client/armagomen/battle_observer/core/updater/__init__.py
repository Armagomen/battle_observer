import os
import re
from collections import namedtuple
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer.core.updater.i18n import getI18n
from armagomen.constants import GLOBAL, URLS, getLogo
from armagomen.utils.common import logInfo, logError, modsPath, gameVersion, urlResponse, getUpdatePath
from armagomen.utils.dialogs import UpdaterDialogs
from armagomen.utils.events import g_events
from gui.Scaleform.Waiting import Waiting
from gui.shared.personality import ServicesLocator
from web.cache.web_downloader import WebDownloader
from wg_async import wg_async, wg_await

WAITING_UPDATE = 'updating'

__NAMES = (
    "UPDATE_CHECKED", "NEW_VERSION", "STARTED", "NEW_FILE", "ALREADY_DOWNLOADED", "FINISHED", "FAILED"
)
__MESSAGES = (
    "The update check is completed, you have the current version.",
    "An update {} is detected, the client will be restarted at the end of the download.",
    "DownloadThread: update started {} at {}",
    "DownloadThread: added new file {}",
    "DownloadThread: update is already downloaded to: {}",
    "DownloadThread: downloading update finished to: {}",
    "DownloadThread: update download failed: {}"
)

LOG_MESSAGES = namedtuple("MESSAGES", __NAMES)(*__MESSAGES)


class DownloadThread(object):
    URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}

    def __init__(self):
        self.version = None
        self.i18n = getI18n()
        self.updateData = dict()
        self.dialogs = UpdaterDialogs()
        self.downloader = None
        self.modPath = os.path.join(modsPath, gameVersion)

    def startDownload(self):
        Waiting.show(WAITING_UPDATE)
        mod_version = self.updateData.get('tag_name', self.version)
        path = os.path.join(getUpdatePath(), mod_version + ".zip")
        if os.path.isfile(path):
            self.extractZipArchive(path)
            logInfo(LOG_MESSAGES.ALREADY_DOWNLOADED.format(path))
            self.dialogs.showUpdateFinished(getLogo() + self.i18n['titleOK'],
                                            self.i18n['messageOK'].format(mod_version))
        else:
            url = self.URLS['last']
            self.downloader = WebDownloader(GLOBAL.ONE)
            if url:
                logInfo(LOG_MESSAGES.STARTED.format(mod_version, url))
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
                    archive.extract(newFile, self.modPath)
                    logInfo(LOG_MESSAGES.NEW_FILE.format(newFile))
        if Waiting.isOpened(WAITING_UPDATE):
            Waiting.hide(WAITING_UPDATE)

    def onDownloaded(self, _url, data):
        self.closeDownloader()
        if data is not None:
            mod_version = self.updateData.get('tag_name', self.version)
            path = os.path.join(getUpdatePath(), mod_version + ".zip")
            with open(path, "wb") as zipArchive:
                zipArchive.write(data)
            logInfo(LOG_MESSAGES.FINISHED.format(path))
            self.extractZipArchive(path)
            self.dialogs.showUpdateFinished(getLogo() + self.i18n['titleOK'],
                                            self.i18n['messageOK'].format(mod_version))
        else:
            self.downloadError(_url)

    def downloadError(self, url):
        if Waiting.isOpened(WAITING_UPDATE):
            Waiting.hide(WAITING_UPDATE)
        message = LOG_MESSAGES.FAILED.format(url)
        logError(message)
        self.dialogs.showUpdateError(message)


class Updater(DownloadThread):

    def __init__(self, version):
        super(Updater, self).__init__()
        self.version = version
        self.inLogin = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.subscribe()

    def request_last_version(self):
        result = False
        response = urlResponse(URLS.UPDATE_GITHUB_API_URL)
        if response:
            self.updateData.update(response)
            new_version = response.get('tag_name', self.version)
            local_ver = self.tupleVersion(self.version)
            server_ver = self.tupleVersion(new_version)
            if local_ver < server_ver:
                assets = response.get('assets')
                for asset in assets:
                    filename = asset.get('name', '')
                    download_url = asset.get('browser_download_url')
                    if filename == 'AutoUpdate.zip':
                        self.URLS['last'] = download_url
                    elif filename.startswith('BattleObserver_'):
                        self.URLS['full'] = download_url
                result = True
                logInfo(LOG_MESSAGES.NEW_VERSION.format(new_version))
            else:
                logInfo(LOG_MESSAGES.UPDATE_CHECKED)
        return result

    @staticmethod
    def tupleVersion(version):
        return tuple(map(int, version.split('.')))

    def subscribe(self):
        result = self.request_last_version()
        if result:
            if self.inLogin:
                g_events.onLoginLoaded += self.showDialog
            else:
                g_events.onHangarLoaded += self.showDialog
        else:
            self.dialogs = None

    @wg_async
    def showDialog(self, view):
        self.dialogs.setView(view)
        title = getLogo() + self.i18n['titleNEW'].format(self.updateData.get('tag_name', self.version))
        gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get("body", GLOBAL.EMPTY_LINE))
        message = self.i18n['messageNEW'].format(self.modPath, gitMessage)
        result = yield wg_await(self.dialogs.showNewVersionAvailable(title, message, self.URLS['full']))
        if result:
            self.startDownload()
        if self.inLogin:
            g_events.onLoginLoaded -= self.showDialog
        else:
            g_events.onHangarLoaded -= self.showDialog
