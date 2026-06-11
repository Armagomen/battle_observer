import json
from collections import defaultdict, namedtuple

from armagomen._constants import GLOBAL
from armagomen.battle_observer.i18n.online import FALLBACK, language, ONLINE, TEXTFORMAT
from armagomen import IALogger
from armagomen.utils.async_request import async_url_request
from armagomen.utils.common import IS_COMMON_TEST
from helpers import dependency
from realm import CURRENT_REALM
from skeletons.connection_mgr import IConnectionManager
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from wg_async import AsyncReturn, wg_async


def getModVersion():
    from armagomen.battle_observer import IBOCore
    core = dependency.instance(IBOCore)
    return core.version


class IBOOnline(object):
    __slots__ = ()

    def fini(self):
        raise NotImplementedError

    @wg_async
    def user_login(self, user_id, name, version):
        raise NotImplementedError

    @wg_async
    def user_logout(self, user_id, attempt=0):
        raise NotImplementedError

    @wg_async
    def get_stats_by_region(self):
        raise NotImplementedError


class Online(IBOOnline):
    connectionMgr = dependency.descriptor(IConnectionManager)
    appLoader = dependency.descriptor(IAppLoader)
    logger = dependency.instance(IALogger)

    MAX_RETRIES = 3
    HEADERS_API = {"apikey": "sb_publishable_Mt1NwMGZHqoj1CG7AkhozQ_XkboVWw1"}
    URLS = namedtuple("URLS", ["user_login", "user_logout", "get_stats_by_region"])(
        "https://ocakppqqnkibvfqqfjol.supabase.co/rest/v1/rpc/user_login_rpc",
        "https://ocakppqqnkibvfqqfjol.supabase.co/rest/v1/rpc/user_logout_rpc",
        "https://ocakppqqnkibvfqqfjol.supabase.co/rest/v1/rpc/get_user_stats_by_region",
    )
    __slots__ = ('online_cache', 'skip_keys', 'userID', 'userName', 'banned')

    def __init__(self):
        self.logger.logInfo("Initializing online stats")
        self.userID = None
        self.userName = None
        self.banned = False
        self.online_cache = defaultdict(lambda: [0, 0])
        self.skip_keys = ('CT', 'null', 'RU')
        self.connectionMgr.onLoggedOn += self._onLoggedOn
        self.appLoader.onGUISpaceEntered += self.showBanned

    def onDisconnected(self):
        if self.userID is not None:
            self.user_logout(self.userID)
            self.userID = None

    def fini(self):
        self.onDisconnected()
        self.online_cache.clear()
        self.connectionMgr.onLoggedOn -= self._onLoggedOn
        self.appLoader.onGUISpaceEntered -= self.showBanned
        self.logger.logInfo("Finished online stats")

    def showBanned(self, spaceID):
        if self.banned and spaceID == GuiGlobalSpaceID.LOBBY:
            from armagomen.utils.dialogs import BannedDialog
            dialog = BannedDialog()
            dialog.show(self.userID, self.userName)
            self.onDisconnected()

    @staticmethod
    def extractDatabaseID(token):
        try:
            return int(str(token).split(":")[0])
        except (IndexError, ValueError, TypeError):
            return None

    def _onLoggedOn(self, responseData):
        if IS_COMMON_TEST:
            return
        self.logger.logDebug("_onLoggedOn: {}", responseData)
        if responseData.get("isDemoAccount", False):
            return
        userID = self.extractDatabaseID(responseData.get('token2'))
        if self.userID != userID and isinstance(userID, int):
            self.onDisconnected()
            self.userID = userID
            self.userName = responseData.get('name')
            self.user_login(userID)

    @wg_async
    def user_login(self, userID):
        data = {
            "user_id": userID,
            "login_name": self.userName,
            "login_version": getModVersion(),
            "login_region": CURRENT_REALM,
            "login_ln_code": language
        }
        response = yield async_url_request(self.URLS.user_login, data=data, headers=self.HEADERS_API, method="POST")
        try:
            body = json.loads(response.body)
            self.banned = body and body[0].get("banned", False)
            self.logger.logInfo("Online: Login response [{}]: banned {}", self.userID, self.banned)
        except Exception as error:
            self.logger.logError("Online: Login body parse error: {}, {}", str(error), response.body)

    @wg_async
    def user_logout(self, user_id, attempt=0):
        data = {"user_id": user_id}
        response = yield async_url_request(self.URLS.user_logout, data=data, headers=self.HEADERS_API, method="POST")
        result = False
        try:
            stats = json.loads(response.body)
            result = stats and stats.get("is_online") is False
            if result:
                self.logger.logInfo("Online: Logout response [{}]: {}", user_id, stats)
            elif attempt < self.MAX_RETRIES:
                result = yield self.user_logout(user_id, attempt=attempt + 1)
            else:
                self.logger.logWarning("Online: Logout failed after {} attempts: {}", self.MAX_RETRIES, user_id)
        except Exception as error:
            self.logger.logError("Online: Logout body parse error: {}, {}", str(error), response.body)
        raise AsyncReturn(result)

    def format_string(self, data):
        filtered = [(region, stats) for region, stats in data.iteritems() if region not in self.skip_keys and isinstance(stats, list)]
        if filtered:
            sorted_items = sorted(filtered, key=lambda item: item[1][1], reverse=True)
            result = GLOBAL.NEW_LINE.join(ONLINE.format(region, *stats) for region, stats in sorted_items)
            return TEXTFORMAT.format(result)
        return FALLBACK

    @wg_async
    def get_stats_by_region(self):
        response = yield async_url_request(self.URLS.get_stats_by_region, headers=self.HEADERS_API, method="POST")
        try:
            self.online_cache.update(json.loads(response.body))
            self.logger.logDebug("online_cache = {}", self.online_cache)
        except Exception as error:
            self.logger.logError("Stats parsing error: {}, {}", str(error), response.body)
        raise AsyncReturn(self.format_string(self.online_cache))
