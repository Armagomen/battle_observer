import os
import re
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer import __version__
from armagomen.battle_observer.core.update.i18n import getI18n, getButtons
from armagomen.constants import GLOBAL, URLS, MESSAGES, getRandomBigLogo
from armagomen.utils.common import logInfo, logError, getCurrentModPath, urlResponse
from armagomen.utils.dialogs import UpdateDialogs
from armagomen.utils.events import g_events
from async import async, await
from gui.Scaleform.Waiting import Waiting
from gui.shared.personality import ServicesLocator
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from web.cache.web_downloader import WebDownloader


class DownloadThread(object):
    URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}
    __slots__ = ("dialogs", "downloader", "updateData", "inLogin", "workingDir", "updateData", "i18n")

    def __init__(self):
        self.i18n = getI18n()
        self.updateData = defaultdict()
        self.dialogs = UpdateDialogs()
        self.downloader = None
        self.workingDir = os.path.join(*getCurrentModPath())

    def startDownload(self):
        info = self.updateData.get('tag_name', __version__)
        url = self.URLS['last']
        Waiting.show('updating')
        self.downloader = WebDownloader(GLOBAL.ONE)
        if info and url:
            logInfo('downloading started {} at {}'.format(info, url))
            self.downloader.download(url, self.onDownloaded)
        else:
            message = 'update {} - download failed: {}'.format(info, url)
            Waiting.hide('updating')
            logError(message)
            self.closeDownloader()
            self.dialogs.showUpdateError(message)

    def closeDownloader(self):
        if self.downloader is not None:
            self.downloader.close()
            self.downloader = None

    def onDownloaded(self, _url, data):
        Waiting.hide('updating')
        logInfo('downloading finished: {}'.format(_url))
        if data is not None:
            old_files = os.listdir(self.workingDir)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, self.workingDir)
        title = getRandomBigLogo() + self.i18n['titleOK']
        message = self.i18n['messageOK'].format(self.updateData.get('tag_name', __version__))
        self.dialogs.showUpdateFinished(title, message, getButtons())
        self.closeDownloader()


class UpdateMain(DownloadThread):
    appLoader = dependency.descriptor(IAppLoader)

    __slots__ = ("dialogs", "downloader", "updateData", "inLogin", "workingDir", "updateData", "i18n")

    def __init__(self):
        super(UpdateMain, self).__init__()
        self.inLogin = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)

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
                g_events.onLoginLoaded += self.showDialog
            else:
                g_events.onHangarLoaded += self.showDialog
        else:
            self.dialogs = None

    @async
    def showDialog(self, view):
        self.dialogs.setView(view)
        title = getRandomBigLogo() + self.i18n['titleNEW'].format(self.updateData.get('tag_name', __version__))
        gitMessage = re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, self.updateData.get("body", GLOBAL.EMPTY_LINE))
        message = self.i18n['messageNEW'].format(self.workingDir, gitMessage)
        result = yield await(self.dialogs.showNewVersionAvailable(title, message, self.URLS, getButtons()))
        if result:
            self.startDownload()
        if self.inLogin:
            g_events.onLoginLoaded -= self.showDialog
        else:
            g_events.onHangarLoaded -= self.showDialog
