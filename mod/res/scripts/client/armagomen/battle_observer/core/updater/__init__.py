import os
import re
import subprocess
from collections import namedtuple
from datetime import datetime, timedelta
from json import loads
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL, URLS
from armagomen.battle_observer.core.updater.i18n import getI18n
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import GAME_VERSION, getObserverCachePath, getUpdatePath, isReplay, MODS_PATH
from armagomen.utils.dialogs import UpdaterDialogs
from armagomen.utils.logging import logDebug, logError, logInfo, logWarning
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
    'DownloadThread: downloading failed: {}'
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
        self.modPath = os.path.join(MODS_PATH, GAME_VERSION)
        self.isReplay = isReplay()
        self.cleanup_exe = os.path.join(getObserverCachePath(), "cleanup_launcher.exe")
        self.cleanup_launcher_exist = os.path.isfile(self.cleanup_exe)
        if not self.cleanup_launcher_exist:
            self.download_cleanup_exe(self.cleanup_exe)

    def download_cleanup_exe(self, local_path):
        downloader = WebDownloader(1)
        exe_url = "https://raw.githubusercontent.com/Armagomen/auto-cleanup-observer/master/dist/cleanup_launcher.exe"

        def onDownload(_url, data):
            if data is not None:
                with open(local_path, 'wb') as out_file:
                    out_file.write(data)
                self.cleanup_launcher_exist = True
            else:
                self.downloadError(_url)
            downloader.close()

        downloader.download(exe_url, onDownload)

    def startDownloadingUpdate(self, version):
        path = os.path.join(getUpdatePath(), version + ".zip")
        if os.path.isfile(path):
            return self.updateFiles(path, version)

        if not self.isReplay:
            Waiting.show(WAITING_UPDATE)
        downloader = WebDownloader(1)

        def onUpdateDownloaded(_url, data):
            if data is not None:
                with open(path, "wb") as zipArchive:
                    zipArchive.write(data)
                logInfo(LOG_MESSAGES.FINISHED, path)
                self.extractZipArchive(path)
                self.showUpdateFinishedDialog(version)
            else:
                self.downloadError(_url)
            if not self.isReplay and Waiting.isOpened(WAITING_UPDATE):
                Waiting.hide(WAITING_UPDATE)
            downloader.close()

        url = URLS.UPDATE + ZIP.format(version)
        logInfo(LOG_MESSAGES.STARTED, version, url)
        downloader.download(url, onUpdateDownloaded)

    def showUpdateFinishedDialog(self, version):
        if self.isReplay:
            return
        git_message = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
        self.dialogs.showUpdateFinished(self.i18n['titleOK'], self.i18n['messageOK'].format(version) + git_message)

    def updateFiles(self, path, version):
        self.extractZipArchive(path)
        self.showUpdateFinishedDialog(version)

    def extractZipArchive(self, path):
        old_files = os.listdir(self.modPath)
        with ZipFile(path) as archive:
            for newFile in archive.namelist():
                if newFile not in old_files:
                    archive.extract(newFile, self.modPath)
                    logInfo(LOG_MESSAGES.NEW_FILE, newFile)

    def fini(self):
        if not self.cleanup_launcher_exist:
            return
        version = self.updateData.get('tag_name', self.version)
        to_delete = [str(os.path.join(self.modPath, old_file))
                     for old_file in os.listdir(self.modPath)
                     if "armagomen.battleObserver_" in old_file and str(version) not in old_file]
        if to_delete:
            logDebug("Try to remove old mod files {} in process {}", to_delete, self.cleanup_exe)
            DETACHED_PROCESS = 0x00000008
            CREATE_NO_WINDOW = 0x08000000
            args = [self.cleanup_exe] + to_delete
            subprocess.Popen(args, creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW, close_fds=True)

    def downloadError(self, url):
        message = LOG_MESSAGES.FAILED.format(url)
        logError(message)
        if not self.isReplay:
            self.dialogs.showUpdateError(message)


class Updater(DownloadThread):

    def __init__(self, modVersion):
        super(Updater, self).__init__()
        self.version = modVersion
        self.timeDelta = datetime.now()

    def start(self):
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        else:
            self.check()

    def fini(self):
        super(Updater, self).fini()
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

    def responseUpdateCheck(self, response):
        if response.responseCode == HTTP_OK_STATUS:
            response_data = loads(response.body)
            self.updateData.update(response_data)
            new_version = response_data.get('tag_name', self.version)
            if self.tupleVersion(self.version) < self.tupleVersion(new_version):
                logInfo(LOG_MESSAGES.NEW_VERSION, new_version)
                if not self.isReplay:
                    self.showUpdateDialog(new_version)
                else:
                    self.startDownloadingUpdate(new_version)
            else:
                logInfo(LOG_MESSAGES.UPDATE_CHECKED)
        elif response.responseCode == 304:
            return
        else:
            logWarning('Updater: contentType={}, responseCode={} body={}', response.contentType, response.responseCode, response.body)

    @wg_async
    def check(self):
        logInfo(LOG_MESSAGES.CHECK)
        response = yield async_url_request(URLS.UPDATE_GITHUB_API_URL)
        self.responseUpdateCheck(response)

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
            self.startDownloadingUpdate(ver)
