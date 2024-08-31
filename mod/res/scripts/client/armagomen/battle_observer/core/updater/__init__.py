import os
import re
from collections import namedtuple
from datetime import datetime, timedelta
from json import loads
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL, URLS
from armagomen.battle_observer.core.updater.i18n import getI18n
from armagomen.utils.common import fetchURL, gameVersion, getUpdatePath, isReplay, modsPath
from armagomen.utils.dialogs import UpdaterDialogs
from armagomen.utils.logging import logError, logInfo, logWarning
from gui.Scaleform.Waiting import Waiting
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from uilogging.core.core_constants import HTTP_OK_STATUS
from web.cache.web_downloader import WebDownloader
from wg_async import wg_async, wg_await

WAITING_UPDATE = 'updating'

__NAMES = (
    'CHECK', 'UPDATE_CHECKED', 'NEW_VERSION', 'STARTED', 'NEW_FILE', 'ALREADY_DOWNLOADED', 'FINISHED', 'FAILED'
)
__MESSAGES = (
    'Checking for an available update.',
    'The update check is completed, you have the current version.',
    'An update {} is detected, the client will be restarted at the end of the download.',
    'DownloadThread: update started {} at {}',
    'DownloadThread: added new file {}',
    'DownloadThread: update is already downloaded to: {}',
    'DownloadThread: downloading update finished to: {}',
    'DownloadThread: update download failed: {}'
)

LOG_MESSAGES = namedtuple("MESSAGES", __NAMES)(*__MESSAGES)
EXE_FILE = "{0}/mod_battle_observer_v{0}.exe"
ZIP = "{0}/AutoUpdate.zip"


class DownloadThread(object):

    def __init__(self):
        self.version = None
        self.i18n = getI18n()
        self.updateData = dict()
        self.dialogs = UpdaterDialogs()
        self.downloader = None
        self.modPath = os.path.join(modsPath, gameVersion)

    def startDownload(self, version):
        path = os.path.join(getUpdatePath(), version + ".zip")
        if os.path.isfile(path):
            self.extractZipArchive(path)
            logInfo(LOG_MESSAGES.ALREADY_DOWNLOADED, path)
            git_message = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
            if not isReplay():
                self.dialogs.showUpdateFinished(self.i18n['titleOK'],
                                                self.i18n['messageOK'].format(version) + git_message)
        else:
            if not isReplay():
                Waiting.show(WAITING_UPDATE)
            url = URLS.UPDATE + ZIP.format(version)
            logInfo(LOG_MESSAGES.STARTED, version, url)
            self.downloader = WebDownloader(GLOBAL.ONE)
            self.downloader.download(url, self.onDownloaded)

    def closeDownloader(self):
        if self.downloader is not None:
            self.downloader.close()
            self.downloader = None

    def extractZipArchive(self, path):
        old_files = os.listdir(self.modPath)
        with ZipFile(path) as archive:
            for newFile in archive.namelist():
                if newFile not in old_files:
                    archive.extract(newFile, self.modPath)
                    logInfo(LOG_MESSAGES.NEW_FILE, newFile)

    def onDownloaded(self, _url, data):
        if data is not None:
            version = self.updateData.get('tag_name', self.version)
            path = os.path.join(getUpdatePath(), version + ".zip")
            with open(path, "wb") as zipArchive:
                zipArchive.write(data)
            logInfo(LOG_MESSAGES.FINISHED, path)
            self.extractZipArchive(path)
            git_message = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
            if not isReplay():
                self.dialogs.showUpdateFinished(self.i18n['titleOK'],
                                                self.i18n['messageOK'].format(version) + git_message)
        else:
            self.downloadError(_url)
        if not isReplay() and Waiting.isOpened(WAITING_UPDATE):
            Waiting.hide(WAITING_UPDATE)
        self.closeDownloader()

    def downloadError(self, url):
        message = LOG_MESSAGES.FAILED.format(url)
        logError(message)
        if not isReplay():
            self.dialogs.showUpdateError(message)


class Updater(DownloadThread):

    def __init__(self, version):
        super(Updater, self).__init__()
        self.timeDelta = datetime.now()
        self.version = version
        if isReplay():
            self.check()
        else:
            ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def responseUpdate(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = loads(response.body)
            self.updateData.update(response_data)
            new_version = response_data.get('tag_name', self.version)
            if self.tupleVersion(self.version) < self.tupleVersion(new_version):
                logInfo(LOG_MESSAGES.NEW_VERSION, new_version)
                if not isReplay():
                    self.showUpdateDialog(new_version)
                else:
                    self.startDownload(new_version)
            else:
                logInfo(LOG_MESSAGES.UPDATE_CHECKED)
        else:
            logWarning('Updater: contentType={}, responseCode={} body={}', response.contentType, response.responseCode,
                       response.body)

    def check(self):
        logInfo(LOG_MESSAGES.CHECK)
        fetchURL(URLS.UPDATE_GITHUB_API_URL, self.responseUpdate)

    @staticmethod
    def tupleVersion(version):
        return tuple(map(int, version.split('.')))

    def onGUISpaceEntered(self, spaceID):
        login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == GuiGlobalSpaceID.LOGIN and login_server_selection or spaceID == GuiGlobalSpaceID.LOBBY:
            current_time = datetime.now()
            if current_time >= self.timeDelta:
                self.timeDelta = current_time + timedelta(hours=1)
                self.check()

    @wg_async
    def showUpdateDialog(self, ver):
        title = self.i18n['titleNEW'].format(self.updateData.get('tag_name', ver))
        git_message = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
        message = self.i18n['messageNEW'].format(self.modPath, git_message)
        handle_url = URLS.UPDATE + EXE_FILE.format(ver)
        result = yield wg_await(self.dialogs.showNewVersionAvailable(title, message, handle_url))
        if result:
            self.startDownload(ver)
