import json
from collections import namedtuple

from armagomen.utils.async_request import async_url_request
from armagomen.utils.logging import logError, logInfo
from helpers import getClientLanguage
from realm import CURRENT_REALM
from wg_async import AsyncReturn, wg_async

SUPABASE_URL = "https://ocakppqqnkibvfqqfjol.supabase.co"

HEADERS_API = {
    "apikey": "sb_publishable_Mt1NwMGZHqoj1CG7AkhozQ_XkboVWw1",
}

URLS = namedtuple("URLS", ["user_login", "user_logout", "get_stats"])(
    SUPABASE_URL + "/rest/v1/rpc/user_login_rpc",
    SUPABASE_URL + "/rest/v1/rpc/user_logout_rpc",
    SUPABASE_URL + "/rest/v1/rpc/get_user_stats",
)


@wg_async
def user_login(user_id, name, version):
    data = {
        "user_id": user_id,
        "login_name": name,
        "login_version": version,
        "login_region": CURRENT_REALM,
        "login_ln_code": getClientLanguage()
    }
    response = yield async_url_request(URLS.user_login, data=data, headers=HEADERS_API, method="POST")
    banned = False
    try:
        body = json.loads(response.body)
        banned = body and body[0].get("banned", False)
        logInfo("Login [{}]: banned {}", user_id, banned)
    except Exception as e:
        logError("Login body parse error: {}, {}", repr(e), response)
    raise AsyncReturn(banned)


@wg_async
def user_logout(user_id):
    data = {"user_id": user_id}
    response = yield async_url_request(URLS.user_logout, data=data, headers=HEADERS_API, method="POST")
    logInfo("Logout [{}]: {}", user_id, response.responseCode)


online_cache = {"online": 0, "total": 0}


@wg_async
def get_stats():
    response = yield async_url_request(URLS.get_stats, headers=HEADERS_API, method="POST")
    try:
        online_cache.update(json.loads(response.body))
    except Exception as e:
        logError("Stats parsing error: {}", repr(e))

    raise AsyncReturn(online_cache)
