import json
import os
import re
import urllib2
from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from armagomen.battle_observer.core.config.hangar.i18n import localization
from armagomen.battle_observer.core.bo_constants import MOD_VERSION, GLOBAL, URLS, MASSAGES, HEADERS
from armagomen.battle_observer.core.update.dialog_button import DialogButtons
from armagomen.utils.common import restartGame, logInfo, openWebBrowser, logError, logWarning, \
    getCurrentModPath
from async import async, await, AsyncReturn
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.DialogsInterface import showDialog
from gui.Scaleform.daapi.view.dialogs import SimpleDialogMeta
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from web.cache.web_downloader import WebDownloader

LAST_UPDATE = defaultdict()
DOWNLOAD_URLS = {"last": None, "full": "https://github.com/Armagomen/battle_observer/releases/latest"}

modsDir, gameVersion = getCurrentModPath()
workingDir = os.path.join(modsDir, gameVersion)


def fixDialogCloseWindow():
    old_dispose = SimpleDialog._dispose

    def closeWindowFix(dialog):
        if len(dialog._SimpleDialog__buttons) >= 2:
            dialog._SimpleDialog__isProcessed = True
        return old_dispose(dialog)

    def onWindowClose(dialog):
        return dialog.destroy()

    SimpleDialog._dispose = closeWindowFix
    SimpleDialog.onWindowClose = onWindowClose


class DialogWindow(object):
    __slots__ = ("localization",)

    def __init__(self):
        self.localization = localization['updateDialog']

    @staticmethod
    def onPressButtonFinished(proceed):
        if proceed:
            restartGame()

    def onPressButtonAvailable(self, proceed):
        if proceed:
            runDownload = DownloadThread()
            runDownload.start()
        else:
            openWebBrowser(DOWNLOAD_URLS['full'])

    def getDialogUpdateFinished(self):
        message = self.localization['messageOK'].format(LAST_UPDATE.get('tag_name', MOD_VERSION))
        title = self.localization['titleOK']
        button = DialogButtons(self.localization['buttonOK'])
        return SimpleDialogMeta(title, message, buttons=button)

    def getDialogNewVersionAvailable(self):
        message = self.localization['messageNEW'].format(LAST_UPDATE.get('tag_name', MOD_VERSION), workingDir)
        gitMessage = LAST_UPDATE.get("body", GLOBAL.EMPTY_LINE)
        message += '<br>{0}'.format(re.sub('^\s+|\r|\t|\s+$', GLOBAL.EMPTY_LINE, gitMessage))
        title = self.localization['titleNEW'].format(LAST_UPDATE.get('tag_name', MOD_VERSION))
        buttons = DialogButtons(self.localization['buttonAUTO'], self.localization['buttonHANDLE'])
        return SimpleDialogMeta(title, message, buttons=buttons)

    def showUpdateFinished(self):
        showDialog(self.getDialogUpdateFinished(), self.onPressButtonFinished)

    def showNewVersionAvailable(self):
        showDialog(self.getDialogNewVersionAvailable(), self.onPressButtonAvailable)


class DownloadThread(object):
    __slots__ = ("downloader",)

    def __init__(self):
        self.downloader = WebDownloader(GLOBAL.ONE)

    def start(self):
        try:
            logInfo('start downloading update {}'.format(LAST_UPDATE.get('tag_name', MOD_VERSION)))
            self.downloader.download(DOWNLOAD_URLS['last'], self.onDownloaded)
        except Exception as error:
            self.downloader.close()
            self.downloader = None
            logError('update {} - download failed: {}'.format(LAST_UPDATE.get('tag_name', MOD_VERSION), repr(error)))

    def onDownloaded(self, _url, data):
        if data is not None:
            old_files = os.listdir(workingDir)
            if GLOBAL.DEBUG_MODE:
                with open(os.path.join(modsDir, 'update.zip'), mode="wb") as f:
                    f.write(data)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, workingDir)
            dialog = DialogWindow()
            dialog.showUpdateFinished()
            logInfo('update downloading finished {}'.format(LAST_UPDATE.get('tag_name', MOD_VERSION)))
        self.downloader.close()
        self.downloader = None


class UpdateMain(object):
    __slots__ = ("screen_to_load",)

    def __init__(self):
        is_login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.screen_to_load = GuiGlobalSpaceID.LOGIN if is_login_server_selection else GuiGlobalSpaceID.LOBBY

    @async
    def request_last_version(self, url):
        def get_update_data():
            try:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
                opener.addheaders = HEADERS
                response = opener.open(url)
                return json.load(response)
            except urllib2.URLError:
                logWarning("Technical problems with the server, please inform the developer.")

        try:
            params = get_update_data()
            if params:
                LAST_UPDATE.update(params)
                new_version = LAST_UPDATE.get('tag_name', MOD_VERSION)
                local_ver = self.tupleVersion(MOD_VERSION)
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
                    ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
                    logInfo(MASSAGES.NEW_VERSION.format(new_version))
                else:
                    logInfo(MASSAGES.UPDATE_CHECKED)
        except Exception:
            LOG_CURRENT_EXCEPTION()
        raise AsyncReturn(True)

    @staticmethod
    def tupleVersion(version):
        return tuple(map(int, version.split(GLOBAL.DOT)))

    @async
    def subscribe(self):
        yield await(self.request_last_version(URLS.UPDATE_GITHUB_API_URL))

    def onGUISpaceEntered(self, spaceID):
        if self.screen_to_load == spaceID:
            self.onNewModVersion()
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

    @staticmethod
    def onNewModVersion():
        fixDialogCloseWindow()
        dialog = DialogWindow()
        dialog.showNewVersionAvailable()
