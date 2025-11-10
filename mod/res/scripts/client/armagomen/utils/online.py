import json
from collections import defaultdict, namedtuple

from armagomen._constants import GLOBAL
from armagomen.battle_observer.i18n.online import FALLBACK, language, ONLINE, TEXTFORMAT
from armagomen.utils.async_request import async_url_request
from armagomen.utils.logging import logDebug, logError, logInfo
from realm import CURRENT_REALM
from wg_async import AsyncReturn, wg_async

SUPABASE_URL = "https://ocakppqqnkibvfqqfjol.supabase.co"

HEADERS_API = {
    "apikey": "sb_publishable_Mt1NwMGZHqoj1CG7AkhozQ_XkboVWw1",
}

URLS = namedtuple("URLS", ["user_login", "user_logout", "get_stats_by_region"])(
    SUPABASE_URL + "/rest/v1/rpc/user_login_rpc",
    SUPABASE_URL + "/rest/v1/rpc/user_logout_rpc",
    SUPABASE_URL + "/rest/v1/rpc/get_user_stats_by_region",
)


@wg_async
def user_login(user_id, name, version):
    data = {
        "user_id": user_id,
        "login_name": name,
        "login_version": version,
        "login_region": CURRENT_REALM,
        "login_ln_code": language
    }
    response = yield async_url_request(URLS.user_login, data=data, headers=HEADERS_API, method="POST")
    banned = False
    try:
        body = json.loads(response.body)
        banned = body and body[0].get("banned", False)
        logInfo("Login response [{}]: banned {}", user_id, banned)
    except Exception as e:
        logError("Login body parse error: {}, {}", repr(e), response.body)
    raise AsyncReturn(banned)


MAX_RETRIES = 3


@wg_async
def user_logout(user_id, attempt=0):
    data = {"user_id": user_id}
    response = yield async_url_request(URLS.user_logout, data=data, headers=HEADERS_API, method="POST")
    result = False
    try:
        stats = json.loads(response.body)
        result = stats and stats.get("is_online") is False
        if result:
            logInfo("Logout response [{}]: {}", user_id, stats)
        elif attempt < MAX_RETRIES:
            result = yield user_logout(user_id, attempt=attempt + 1)
        else:
            logError("Logout failed after {} attempts: {}", MAX_RETRIES, user_id)
    except Exception as e:
        logError("Response parsing error: {}, {}", repr(e), response.body)
    raise AsyncReturn(result)


online_cache = defaultdict(lambda: [0, 0])
skip_keys = ('CT', 'null', 'RU')


def format_string(data):
    filtered = [(region, stats) for region, stats in data.iteritems() if region not in skip_keys and isinstance(stats, list)]
    if filtered:
        sorted_items = sorted(filtered, key=lambda item: item[1][1], reverse=True)
        result = GLOBAL.NEW_LINE.join(ONLINE.format(region, *stats) for region, stats in sorted_items)
        return TEXTFORMAT.format(result)
    return FALLBACK


@wg_async
def get_stats_by_region():
    response = yield async_url_request(URLS.get_stats_by_region, headers=HEADERS_API, method="POST")
    try:
        online_cache.update(json.loads(response.body))
        logDebug("online_cache = {}", online_cache)
    except Exception as e:
        logError("Stats parsing error: {}, {}", repr(e), response.body)
    raise AsyncReturn(format_string(online_cache))
