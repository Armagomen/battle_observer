import os
from base64 import b64decode as decode_string
from io import BytesIO
from zipfile import ZipFile

from account_helpers.settings_core.settings_constants import GAME
from gui.DialogsInterface import showDialog
from gui.Scaleform.daapi.view.dialogs import SimpleDialogMeta
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID
from web.cache.web_downloader import WebDownloader
from .bo_constants import MOD_VERSION, GLOBAL, URLS, MASSAGES
from .bw_utils import restartGame, logInfo, openWebBrowser, logError
from .core import m_core
from .dialog_button import DialogButtons
from .events import g_events
from ..hangar.i18n.localization_getter import localization


def fixDialogCloseWindow():
    old_dispose = SimpleDialog._dispose

    def closeWindowFix(dialog):
        if len(dialog._SimpleDialog__buttons) >= 2:
            dialog._SimpleDialog__isProcessed = True
        old_dispose(dialog)

    def onWindowClose(dialog):
        dialog.destroy()

    SimpleDialog._dispose = closeWindowFix
    SimpleDialog.onWindowClose = onWindowClose


class DialogWindow(object):
    def __init__(self, ver):
        self.localization = localization['updateDialog']
        self.newVer = ver

    @staticmethod
    def onPressButtonFinished(proceed):
        if proceed:
            restartGame()

    def onPressButtonAvailable(self, proceed):
        if proceed:
            runDownload = DownloadThread(self.newVer)
            runDownload.start()
        else:
            openWebBrowser(decode_string(URLS.UPDATE_URL))

    def getDialogUpdateFinished(self):
        message = self.localization['messageOK'].format(self.newVer)
        title = self.localization['titleOK']
        button = DialogButtons(self.localization['buttonOK'])
        return SimpleDialogMeta(title, message, buttons=button)

    def getDialogNewVersionAvailable(self):
        message = self.localization['messageNEW'].format(self.newVer, m_core.workingDir)
        title = self.localization['titleNEW'].format(self.newVer)
        buttons = DialogButtons(self.localization['buttonAUTO'], self.localization['buttonHANDLE'])
        return SimpleDialogMeta(title, message, buttons=buttons)

    def showUpdateFinished(self):
        showDialog(self.getDialogUpdateFinished(), self.onPressButtonFinished)

    def showNewVersionAvailable(self):
        showDialog(self.getDialogNewVersionAvailable(), self.onPressButtonAvailable)


class DownloadThread(object):
    def __init__(self, ver):
        self.newVer = ver
        self.downloader = WebDownloader(GLOBAL.ONE)

    def start(self):
        # noinspection PyBroadException
        try:
            logInfo('start downloading update {}'.format(self.newVer))
            self.downloader.download(decode_string(URLS.UPDATE_URL), self.onDownloaded)
        except Exception as error:
            self.downloader.close()
            self.downloader = None
            logError('update {} - download failed: {}'.format(self.newVer, repr(error)))

    def onDownloaded(self, _url, data):
        if data is not None:
            old_files = os.listdir(m_core.workingDir)
            if GLOBAL.DEBUG_MODE:
                with open(os.path.join(m_core.modsDir, "Battle_Observer_Update_temp_debug.zip"), mode="wb") as f:
                    f.write(data)
            with BytesIO(data) as zip_file, ZipFile(zip_file) as archive:
                for newFile in archive.namelist():
                    if newFile not in old_files:
                        logInfo('update, add new file {}'.format(newFile))
                        archive.extract(newFile, m_core.workingDir)
            dialog = DialogWindow(self.newVer)
            dialog.showUpdateFinished()
            logInfo('update downloading finished {}'.format(self.newVer))
        self.downloader.close()
        self.downloader = None


class CheckUpdate(object):

    def __init__(self):
        self.newVer = MOD_VERSION
        self.downloader = WebDownloader(GLOBAL.ONE)

    @staticmethod
    def tupleVersion(version):
        return tuple(map(int, version.split(GLOBAL.DOT)))

    def start(self):
        # noinspection PyBroadException
        try:
            self.downloader.download(decode_string(URLS.CHECK_VERSION_URL), self.onDownloaded)
        except Exception as error:
            self.downloader.close()
            self.downloader = None
            logError("version check failed: {}".format(repr(error)))

    def onDownloaded(self, _url, data):
        if data is not None:
            version = data
            if version is not None:
                self.newVer = version.strip()
                local_ver = self.tupleVersion(MOD_VERSION)
                server_ver = self.tupleVersion(self.newVer)
                if local_ver < server_ver:
                    if not GLOBAL.DEBUG_MODE:
                        g_events.onNewModVersion(self.newVer)
                    logInfo(MASSAGES.NEW_VERSION.format(self.newVer))
                else:
                    logInfo(MASSAGES.UPDATE_CHECKED)
        self.downloader.close()
        self.downloader = None


class UpdateMain(object):

    def __init__(self):
        is_login_server_selection = ServicesLocator.settingsCore.getSetting(GAME.LOGIN_SERVER_SELECTION)
        self.screen_to_load = GuiGlobalSpaceID.LOGIN if is_login_server_selection else GuiGlobalSpaceID.LOBBY

    def subscribe(self):
        ServicesLocator.appLoader.onGUISpaceEntered += self.onGUISpaceEntered
        g_events.onNewModVersion += self.onNewModVersion

    def onGUISpaceEntered(self, spaceID):
        if self.screen_to_load == spaceID:
            check = CheckUpdate()
            check.start()
            if GLOBAL.DEBUG_MODE:
                self.onNewModVersion(MOD_VERSION)
            ServicesLocator.appLoader.onGUISpaceEntered -= self.onGUISpaceEntered

    def onNewModVersion(self, version):
        fixDialogCloseWindow()
        dialog = DialogWindow(version)
        dialog.showNewVersionAvailable()
        g_events.onNewModVersion -= self.onNewModVersion


g_update = UpdateMain()
