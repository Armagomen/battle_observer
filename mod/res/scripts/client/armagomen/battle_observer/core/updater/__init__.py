# coding=utf-8
import fnmatch
import os
import re
import subprocess
import threading
from collections import namedtuple
from json import loads
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL, URLS
from armagomen.battle_observer.i18n.updater import LOCALIZED_BY_LANG
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import CURRENT_MODS_DIR, getObserverCachePath, getUpdatePath, isReplay, MODS_DIR
from armagomen.utils.dialogs import UpdaterDialogs
from armagomen.utils.logging import logDebug, logError, logInfo, logWarning
from datetime import datetime, timedelta
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

LOG_MESSAGES = namedtuple("MESSAGES", __NAMES)(*LOCALIZED_BY_LANG["messages"])
EXE_FILE = "{0}/mod_battle_observer_v{0}.exe"
ZIP = "{0}/AutoUpdate.zip"
DETACHED_NO_WINDOW = 0x08000008
WOTMOD_PATTERN = "armagomen.battleObserver_*.wotmod"


def download_and_write(url, local_path, on_success, on_failure):
    downloader = WebDownloader(1)

    def onDownloaded(_url, data):
        if data is not None:
            with open(local_path, 'wb') as out_file:
                out_file.write(data)
            on_success()
        else:
            on_failure(_url)
        downloader.close()

    downloader.download(url, onDownloaded)


def tupleVersion(version):
    return tuple(map(int, version.split('.')))


class Updater(object):

    def __init__(self, modVersion):
        super(Updater, self).__init__()
        self.cleanup_exe = os.path.join(getObserverCachePath(), "cleanup_launcher.exe")
        self.cleanup_launcher_exist = os.path.isfile(self.cleanup_exe)
        self.dialogs = UpdaterDialogs()
        self.isLobby = False
        self.isReplay = isReplay()
        self.timeDelta = datetime.now()
        self.updateData = dict()
        self.version = modVersion
        self.gitMessage = ""
        if not self.cleanup_launcher_exist:
            self.download_cleanup_exe(self.cleanup_exe)

    def download_cleanup_exe(self, local_path):
        url = "https://raw.githubusercontent.com/Armagomen/auto-cleanup-observer/master/dist/cleanup_launcher.exe"

        def success():
            self.cleanup_launcher_exist = True

        download_and_write(url, local_path, success, logError)

    def start(self):
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        else:
            self.check()

    def setWaitingState(self, targetState):
        if self.isReplay:
            return
        if targetState != Waiting.isOpened(WAITING_UPDATE):
            if targetState:
                Waiting.show(WAITING_UPDATE)
            else:
                Waiting.hide(WAITING_UPDATE)

    def startDownloadingUpdate(self, version):
        path = os.path.join(getUpdatePath(), version + ".zip")
        if os.path.isfile(path):
            return self.updateFiles(path, version)
        self.setWaitingState(True)
        url = URLS.UPDATE + ZIP.format(version)
        logInfo(LOG_MESSAGES.STARTED, version, url)

        def success():
            logInfo(LOG_MESSAGES.FINISHED, path)
            self.setWaitingState(False)
            self.updateFiles(path, version)

        def failure(_url):
            self.setWaitingState(False)
            self.downloadError(_url)

        download_and_write(url, path, success, failure)

    def showUpdateFinishedDialog(self, version):
        if self.isReplay:
            return
        self.dialogs.showUpdateFinished(LOCALIZED_BY_LANG['titleOK'], LOCALIZED_BY_LANG['messageOK'].format(version) + self.gitMessage,
                                        self.isLobby)

    def updateFiles(self, path, version):
        self.extractZipArchive(path)
        self.showUpdateFinishedDialog(version)

    @staticmethod
    def extractZipArchive(path):
        old_files = os.listdir(CURRENT_MODS_DIR)
        with ZipFile(path) as archive:
            for newFile in archive.namelist():
                if newFile not in old_files:
                    archive.extract(newFile, CURRENT_MODS_DIR)
                    logInfo(LOG_MESSAGES.NEW_FILE, newFile)

    def downloadError(self, url):
        message = LOG_MESSAGES.FAILED.format(url)
        logError(message)
        if not self.isReplay:
            self.dialogs.showUpdateError(message, self.isLobby)

    def fini(self):
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
        if self.cleanup_launcher_exist:
            self.checkAndStartCleanup()

    @staticmethod
    def parseFullVersion(path):
        mod_version = re.search(r'mods[\\/](\d+(?:\.\d+)+)', path).group(1)
        file_version = re.search(r'battleObserver_(\d+(?:\.\d+)+)\.wotmod', path).group(1)
        return tupleVersion(mod_version), tupleVersion(file_version)

    @staticmethod
    def findObserverMods():
        for root, dirs, files in os.walk(MODS_DIR):
            for name in files:
                if fnmatch.fnmatch(name, WOTMOD_PATTERN):
                    yield os.path.join(root, name)

    def checkAndStartCleanup(self):
        mod_files = sorted(self.findObserverMods(), key=self.parseFullVersion)
        mod_files.pop(-1)
        if mod_files:
            logInfo("Remove old versions >> {}", mod_files)
            t = threading.Thread(target=self._cleanup_worker, args=(mod_files,))
            t.daemon = True
            t.start()

    def _cleanup_worker(self, mod_files):
        logDebug("Try to remove old mod files {} in process {}", mod_files, self.cleanup_exe)
        mod_files.insert(0, self.cleanup_exe)
        subprocess.Popen(mod_files, creationflags=DETACHED_NO_WINDOW)

    def responseUpdateCheck(self, response):
        response_data = loads(response.body)
        self.updateData.update(response_data)
        self.gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
        new_version = response_data.get('tag_name', self.version)
        if tupleVersion(self.version) < tupleVersion(new_version):
            logInfo(LOG_MESSAGES.NEW_VERSION, new_version)
            if not self.isReplay:
                self.showUpdateDialog(new_version)
            else:
                self.startDownloadingUpdate(new_version)
        else:
            logInfo(LOG_MESSAGES.UPDATE_CHECKED)

    @wg_async
    def check(self):
        logInfo(LOG_MESSAGES.CHECK)
        response = yield async_url_request(URLS.UPDATE_GITHUB_API_URL)
        if response.responseCode == HTTP_OK_STATUS:
            self.responseUpdateCheck(response)
        elif response.responseCode != 304:
            logWarning('Updater: contentType={}, responseCode={} body={}', response.contentType, response.responseCode, response.body)

    def onGUISpaceEntered(self, spaceID):
        self.isLobby = spaceID == GuiGlobalSpaceID.LOBBY
        login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == GuiGlobalSpaceID.LOGIN and login_server_selection or self.isLobby:
            current_time = datetime.now()
            if current_time >= self.timeDelta:
                self.timeDelta = current_time + timedelta(hours=1)
                self.check()

    @wg_async
    def showUpdateDialog(self, version):
        title = LOCALIZED_BY_LANG['titleNEW'].format(version)
        message = LOCALIZED_BY_LANG['messageNEW'].format(CURRENT_MODS_DIR, self.gitMessage)
        handle_url = URLS.UPDATE + EXE_FILE.format(version)
        result = yield wg_await(self.dialogs.showNewVersionAvailable(title, message, handle_url, self.isLobby))
        if result:
            self.startDownloadingUpdate(version)
