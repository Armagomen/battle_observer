# coding=utf-8
import fnmatch
import os
import re
import subprocess
import threading
from collections import namedtuple
from datetime import datetime, timedelta
from json import loads
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL, URLS
from armagomen.battle_observer.i18n.updater import LOCALIZED_BY_LANG
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

LOG_MESSAGES = namedtuple("MESSAGES", __NAMES)(*LOCALIZED_BY_LANG["messages"])
EXE_FILE = "{0}/mod_battle_observer_v{0}.exe"
ZIP = "{0}/AutoUpdate.zip"


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
        self.modsPath = os.path.join(MODS_PATH, GAME_VERSION)
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

    def extractZipArchive(self, path):
        old_files = os.listdir(self.modsPath)
        with ZipFile(path) as archive:
            for newFile in archive.namelist():
                if newFile not in old_files:
                    archive.extract(newFile, self.modsPath)
                    logInfo(LOG_MESSAGES.NEW_FILE, newFile)

    def downloadError(self, url):
        message = LOG_MESSAGES.FAILED.format(url)
        logError(message)
        if not self.isReplay:
            self.dialogs.showUpdateError(message, self.isLobby)

    def fini(self):
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
        if not self.cleanup_launcher_exist:
            return
        self.checkAndStartCleanup()

    @staticmethod
    def parseVersion(f):
        return tupleVersion(f.split('_')[1].rsplit('.', 1)[0])

    def checkAndStartCleanup(self):
        to_delete = sorted(fnmatch.filter(os.listdir(self.modsPath), "armagomen.battleObserver_*.wotmod"), key=self.parseVersion)[:-1]
        if to_delete:
            logInfo("Remove old versions >> {}", to_delete)
            t = threading.Thread(target=self._cleanup_worker, args=([os.path.join(self.modsPath, f) for f in to_delete],))
            t.daemon = True
            t.start()

    def _cleanup_worker(self, to_delete):
        logDebug("Try to remove old mod files {} in process {}", to_delete, self.cleanup_exe)
        DETACHED_PROCESS = 0x00000008
        CREATE_NO_WINDOW = 0x08000000
        args = [self.cleanup_exe] + to_delete
        subprocess.Popen(args, creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW, close_fds=True)

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
        login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == GuiGlobalSpaceID.LOGIN and login_server_selection or spaceID == GuiGlobalSpaceID.LOBBY:
            self.isLobby = spaceID == GuiGlobalSpaceID.LOBBY
            current_time = datetime.now()
            if current_time >= self.timeDelta:
                self.timeDelta = current_time + timedelta(hours=1)
                self.check()

    @wg_async
    def showUpdateDialog(self, version):
        title = LOCALIZED_BY_LANG['titleNEW'].format(version)
        message = LOCALIZED_BY_LANG['messageNEW'].format(self.modsPath, self.gitMessage)
        handle_url = URLS.UPDATE + EXE_FILE.format(version)
        result = yield wg_await(self.dialogs.showNewVersionAvailable(title, message, handle_url, self.isLobby))
        if result:
            self.startDownloadingUpdate(version)
