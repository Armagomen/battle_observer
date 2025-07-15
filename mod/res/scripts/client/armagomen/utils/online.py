import json

from armagomen.utils.async_request import async_url_request
from armagomen.utils.logging import logError, logInfo
from helpers import getClientLanguage
from realm import CURRENT_REALM
from wg_async import AsyncReturn, wg_async

SUPABASE_URL = "https://ocakppqqnkibvfqqfjol.supabase.co"

headers_common = {
    "apikey": "sb_publishable_Mt1NwMGZHqoj1CG7AkhozQ_XkboVWw1",
}


@wg_async
def user_login(user_id, name, version):
    url = SUPABASE_URL + "/rest/v1/users?select=banned"
    headers = headers_common.copy()
    headers["Prefer"] = "resolution=merge-duplicates,return=representation"
    data = {
        "id": user_id,
        "name": name,
        "region": CURRENT_REALM,
        "ln_code": getClientLanguage().upper(),
        "is_online": True,
        "version": version
    }
    response = yield async_url_request(url, data=data, headers=headers, method="POST")
    banned = False
    try:
        body = json.loads(response.body)
        banned = body and body[0].get("banned", False)
        logInfo("Login [{}]: {}", user_id, body)
    except Exception as e:
        logError("Login body parse error: {}", e)
    raise AsyncReturn(banned)


@wg_async
def user_logout(user_id):
    url = SUPABASE_URL + "/rest/v1/users?id=eq.{}".format(user_id)
    headers = headers_common.copy()
    headers["Prefer"] = "return=minimal"
    data = {"is_online": False}
    response = yield async_url_request(url, data=data, headers=headers, method="PATCH")
    logInfo("Logout [{}]: {}", user_id, response.responseCode)


@wg_async
def get_stats():
    url = SUPABASE_URL + "/rest/v1/rpc/get_user_stats"
    response = yield async_url_request(url, headers=headers_common.copy(), method="POST")
    try:
        result = json.loads(response.body)
        online = result.get("online", 0)
        total = result.get("total", 0)
    except Exception as e:
        logError("Stats parsing error: {}", repr(e))
        online = total = 0

    raise AsyncReturn((online, total))
