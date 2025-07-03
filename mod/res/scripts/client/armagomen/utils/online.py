import json

from armagomen.utils.async_request import async_url_request
from armagomen.utils.logging import logDebug, logError
from helpers import getClientLanguage
from realm import CURRENT_REALM
from wg_async import AsyncReturn, wg_async

SUPABASE_URL = "https://ocakppqqnkibvfqqfjol.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jYWtwcHFxbmtpYnZmcXFmam9sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzOTAzMDUsImV4cCI6MjA2Njk2NjMwNX0.epik_9pG5mwUGqDFQby41k4g5Qg-oKiowFJP40nWVD4"

headers_common = {
    "apikey": SUPABASE_KEY,
    "Authorization": "Bearer " + SUPABASE_KEY,
}


@wg_async
def user_login(user_id, name, version):
    url = SUPABASE_URL + "/rest/v1/users"
    headers = headers_common.copy()
    headers["Prefer"] = "resolution=merge-duplicates,return=minimal"
    data = {
        "id": user_id,
        "name": name,
        "region": CURRENT_REALM,
        "ln_code": getClientLanguage().upper(),
        "is_online": True,
        "version": version
    }
    response = yield async_url_request(url, data=data, headers=headers, method="POST")
    logDebug("Login [{}]: {}", user_id, response.responseCode)


@wg_async
def user_logout(user_id):
    url = SUPABASE_URL + "/rest/v1/users?id=eq.{}".format(user_id)
    headers = headers_common.copy()
    headers["Prefer"] = "return=minimal"
    data = {"is_online": False}
    response = yield async_url_request(url, data=data, headers=headers, method="PATCH")
    logDebug("Logout [{}]: {}", user_id, response.responseCode)


@wg_async
def get_stats():
    url = SUPABASE_URL + "/rest/v1/rpc/get_user_stats"
    response = yield async_url_request(url, headers=headers_common, method="POST")
    try:
        result = json.loads(response.body)
        online = result.get("online", 0)
        total = result.get("total", 0)
    except Exception as e:
        logError("Stats parsing error: {}", repr(e))
        online = total = 0

    raise AsyncReturn((online, total))
