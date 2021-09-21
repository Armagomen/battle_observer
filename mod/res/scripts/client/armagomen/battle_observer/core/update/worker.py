import json
import os
import re
import urllib2
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer import __version__
from armagomen.battle_observer.settings.hangar.i18n import localization
from armagomen.constants import GLOBAL, URLS, MESSAGES, HEADERS
from armagomen.utils.common import restartGame, logInfo, openWebBrowser, logError, logWarning, \
    getCurrentModPath
from async import async, await, AsyncReturn
from gui.impl.dialogs import dialogs
from gui.impl.dialogs.builders import InfoDialogBuilder, WarningDialogBuilder
from gui.impl.pub.dialog_window import DialogButtons
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from web.cache.web_downloader import WebDownloader

LAST_UPDATE = defaultdict()
DOWNLOAD_URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}

workingDir = os.path.join(*getCurrentModPath())


class DialogWindow(object):
    __slots__ = ("localization",)

    def __init__(self):
        self.localization = localization['updateDialog']

    def getFinishedBuilder(self):
        message = self.localization['messageOK'].format(LAST_UPDATE.get('tag_name', __version__))
        builder = WarningDialogBuilder()
        builder.setFormattedTitle(self.localization['titleOK'])
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.PURCHASE, "Restart", True, rawLabel=self.localization['buttonOK'])
        builder.addButton(DialogButtons.CANCEL, "Cancel", False, rawLabel=self.localization['buttonCancel'])
        return builder

    def getNewVersionBuilder(self):
        message = self.localization['messageNEW'].format(workingDir)
        gitMessage = LAST_UPDATE.get("body", GLOBAL.EMPTY_LINE)
        message += '\n\n{0}'.format(re.sub(r'^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, gitMessage))
        builder = InfoDialogBuilder()
        builder.setFormattedTitle(self.localization['titleNEW'].format(LAST_UPDATE.get('tag_name', __version__)))
        builder.setFormattedMessage(message)
        builder.addButton(DialogButtons.RESEARCH, "Automatic", True, rawLabel=self.localization['buttonAUTO'])
        builder.addButton(DialogButtons.PURCHASE, "Manually", False, rawLabel=self.localization['buttonHANDLE'])
        builder.addButton(DialogButtons.CANCEL, "Cancel", False, rawLabel=self.localization['buttonCancel'])
        return builder

    @async
    def showUpdateFinished(self):
        result = yield await(dialogs.showSimple(self.getFinishedBuilder().build(), DialogButtons.PURCHASE))
        if result:
            restartGame()
        raise AsyncReturn(result)

    @async
    def showNewVersionAvailable(self):
        result = yield await(dialogs.show(self.getNewVersionBuilder().build()))
        if result.result == DialogButtons.RESEARCH:
            runDownload = DownloadThread()
            runDownload.start()
            raise AsyncReturn(True)
        elif result.result == DialogButtons.PURCHASE:
            openWebBrowser(DOWNLOAD_URLS['full'])
            raise AsyncReturn(True)
        else:
            raise AsyncReturn(False)


class DownloadThread(object):
    __slots__ = ("downloader",)

    def __init__(self):
        self.downloader = WebDownloader(GLOBAL.ONE)

    def start(self):
        try:
            logInfo('start downloading update {}'.format(LAST_UPDATE.get('tag_name', __version__)))
            self.downloader.download(DOWNLOAD_URLS['last'], self.onDownloaded)
        except Exception as error:
            self.downloader.close()
            self.downloader = None
            logError('update {} - download failed: {}'.format(LAST_UPDATE.get('tag_name', __version__), repr(error)))

    def onDownloaded(self, _url, data):
        if data is not None:
            old_files = os.listdir(workingDir)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, workingDir)
            dialog = DialogWindow()
            dialog.showUpdateFinished()
            logInfo('update downloading finished {}'.format(LAST_UPDATE.get('tag_name', __version__)))
        self.downloader.close()
        self.downloader = None


class UpdateMain(object):
    __slots__ = ("screen_to_load",)

    def __init__(self):
        is_login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.screen_to_load = GuiGlobalSpaceID.LOGIN if is_login_server_selection else GuiGlobalSpaceID.LOBBY

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
            ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered

    def onGUISpaceEntered(self, spaceID):
        if self.screen_to_load == spaceID:
            dialog = DialogWindow()
            dialog.showNewVersionAvailable()
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered
