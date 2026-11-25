# coding=utf-8
import fnmatch
import os
import re
from collections import namedtuple
from json import loads
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen._constants import GLOBAL, URLS
from armagomen._logger import IALogger
from armagomen.battle_observer.i18n.updater import LOCALIZED_BY_LANG
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import GAME_VERSION, getObserverCachePath, getUpdatePath, joinAndNormalizePath, MODS_DIR, VERSIONED_MODS_DIR
from armagomen.utils.dialogs import UpdaterDialogs
from BattleReplay import isLoading, isPlaying
from datetime import datetime, timedelta
from gui.Scaleform.Waiting import Waiting
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID
from uilogging.core.core_constants import HTTP_OK_STATUS
from web.cache.web_downloader import WebDownloader
from wg_async import wg_async, wg_await

WAITING_UPDATE = 'updating'

__NAMES = ('CHECK', 'UPDATE_CHECKED', 'NEW_VERSION', 'STARTED', 'NEW_FILE', 'ALREADY_DOWNLOADED', 'FINISHED', 'FAILED')
LOG_MESSAGES = namedtuple("MESSAGES", __NAMES)(*LOCALIZED_BY_LANG["messages"])

EXE_FILE = "{0}/mod_battle_observer_v{0}.exe"
ZIP = "{0}/AutoUpdate.zip"
CREATE_NO_WINDOW = 0x08000000
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
    match = re.search(r'\d+(?:\.\d+)+', version)
    if not match:
        return (0,)
    return tuple(map(int, match.group().split('.')))


class IBOUpdater(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError


class Updater(IBOUpdater):
    logger = dependency.descriptor(IALogger)

    @property
    def isReplay(self):
        return isLoading() or isPlaying()

    def __init__(self, modVersion):
        super(Updater, self).__init__()
        self.logger.logInfo('Initializing Updater')
        self.dialogs = UpdaterDialogs()
        self.isLobby = False
        self.timeDelta = datetime.now()
        self.updateData = dict()
        self.version = modVersion
        self.gitMessage = ""
        self.__finished = False
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
            self.updateFiles(path, version)
            return
        self.setWaitingState(True)
        url = URLS.UPDATE + ZIP.format(version)
        self.logger.logInfo(LOG_MESSAGES.STARTED, version, url)

        def success():
            self.logger.logInfo(LOG_MESSAGES.FINISHED, path)
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
        self.version = version

    def extractZipArchive(self, path):
        with ZipFile(path) as archive:
            for newFile in archive.namelist():
                if newFile.endswith('/') or os.path.exists(joinAndNormalizePath(VERSIONED_MODS_DIR, newFile)):
                    continue
                archive.extract(newFile, VERSIONED_MODS_DIR)
                self.logger.logInfo(LOG_MESSAGES.NEW_FILE, newFile)

    def downloadError(self, url):
        message = LOG_MESSAGES.FAILED.format(url)
        self.logger.logError(message)
        if not self.isReplay:
            self.dialogs.showUpdateError(message, self.isLobby)

    def fini(self):
        if not self.isReplay:
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

        cleanup_exe = os.path.join(getObserverCachePath(), "cleanup_launcher.exe")
        if os.path.isfile(cleanup_exe):
            os.remove(cleanup_exe)

        outdate_mod_files = tuple(self.findOutdateVersions(self.version))
        if outdate_mod_files:
            self.schedule_cleanup_on_exit(outdate_mod_files)
            self.logger.logInfo("Updater: scheduled cleanup for {} files", outdate_mod_files)

        self.logger.logInfo("Finished Updater")
        self.__finished = True

    @staticmethod
    def checkRoot(root):
        root_version = re.search(r'mods[\\/](\d+(?:\.\d+)+)', root).group(1)
        return tupleVersion(root_version) >= tupleVersion(GAME_VERSION)

    def findOutdateVersions(self, currentVersion):
        for root, dirs, files in os.walk(MODS_DIR):
            for name in files:
                if fnmatch.fnmatch(name, WOTMOD_PATTERN):
                    if currentVersion in name.lower() and self.checkRoot(root):
                        continue
                    yield os.path.join(root, name)

    def responseUpdateCheck(self, response):
        if self.__finished:
            return
        response_data = loads(response.body)
        self.updateData.update(response_data)
        self.gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get('body', GLOBAL.EMPTY_LINE))
        new_version = response_data.get('tag_name', self.version)
        if tupleVersion(self.version) < tupleVersion(new_version):
            self.logger.logInfo(LOG_MESSAGES.NEW_VERSION, new_version)
            if not self.isReplay:
                self.showUpdateDialog(new_version)
            else:
                self.startDownloadingUpdate(new_version)
        else:
            self.logger.logInfo(LOG_MESSAGES.UPDATE_CHECKED)

    @wg_async
    def check(self):
        if self.__finished:
            return
        self.logger.logInfo(LOG_MESSAGES.CHECK)
        response = yield async_url_request(URLS.UPDATE_GITHUB_API_URL)
        if response.responseCode == HTTP_OK_STATUS:
            self.responseUpdateCheck(response)
        elif response.responseCode != 304:
            self.logger.logWarning('Updater: contentType={}, responseCode={} body={}', response.contentType, response.responseCode,
                                   response.body)

    def onGUISpaceEntered(self, spaceID):
        self.isLobby = spaceID == GuiGlobalSpaceID.LOBBY
        login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        if spaceID == GuiGlobalSpaceID.LOGIN and login_server_selection or self.isLobby:
            current_time = datetime.now()
            if current_time >= self.timeDelta:
                self.timeDelta = current_time + timedelta(hours=2)
                self.check()

    @wg_async
    def showUpdateDialog(self, version):
        title = LOCALIZED_BY_LANG['titleNEW'].format(version)
        message = LOCALIZED_BY_LANG['messageNEW'].format(VERSIONED_MODS_DIR, self.gitMessage)
        handle_url = URLS.UPDATE + EXE_FILE.format(version)
        result = yield wg_await(self.dialogs.showNewVersionAvailable(title, message, handle_url, self.isLobby))
        if result:
            self.startDownloadingUpdate(version)

    @staticmethod
    def schedule_cleanup_on_exit(filepaths):
        ps_paths = ', '.join("'{}'".format(p.replace("'", "''")) for p in filepaths)
        if not ps_paths:
            return
        from subprocess import Popen

        ps_script = (
            "Wait-Process -Id {0} -ErrorAction SilentlyContinue; "
            "Remove-Item -LiteralPath @({1}) -Force -ErrorAction SilentlyContinue"
        ).format(os.getpid(), ps_paths)

        Popen(
            ['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
            creationflags=CREATE_NO_WINDOW,
            close_fds=True
        )
