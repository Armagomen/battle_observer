import json
import urllib2

from armagomen.utils.logging import logDebug, logError
from helpers import getClientLanguage
from realm import CURRENT_REALM

SUPABASE_URL = "https://ocakppqqnkibvfqqfjol.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jYWtwcHFxbmtpYnZmcXFmam9sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzOTAzMDUsImV4cCI6MjA2Njk2NjMwNX0.epik_9pG5mwUGqDFQby41k4g5Qg-oKiowFJP40nWVD4"

headers_common = {
    "apikey": SUPABASE_KEY,
    "Authorization": "Bearer " + SUPABASE_KEY,
    "Content-Type": "application/json"
}


def user_login(user_id, name):
    url = SUPABASE_URL + "/rest/v1/users"
    headers = headers_common.copy()
    headers["Prefer"] = "resolution=merge-duplicates,return=minimal"

    data = {
        "id": user_id,
        "name": name,
        "region": CURRENT_REALM,
        "ln_code": getClientLanguage().upper(),
        "is_online": True
    }

    req = urllib2.Request(url, json.dumps(data), headers)
    req.get_method = lambda: "POST"

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        logDebug("Minimal response code for user {}: {}", user_id, code)
    except Exception as e:
        logError("Login failed for user {}: {}", user_id, e)


def user_logout(user_id):
    url = SUPABASE_URL + "/rest/v1/users?id=eq." + str(user_id)
    headers = headers_common.copy()
    headers["Prefer"] = "return=minimal"

    data = {
        "is_online": False
    }

    req = urllib2.Request(url, json.dumps(data), headers)
    req.get_method = lambda: "PATCH"

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()
        logDebug("Minimal response code for user {}: {}", user_id, code)
    except Exception as e:
        logError("Logout failed for user {}: {}", user_id, e)


def get_stats():
    try:
        url = SUPABASE_URL + "/rest/v1/rpc/get_user_stats"
        req = urllib2.Request(url, "{}", headers_common)
        req.get_method = lambda: "POST"

        res = urllib2.urlopen(req)
        data = json.loads(res.read())
        return data["online"], data["total"]

    except Exception as e:
        logError("Unable to fetch Supabase statistics: {}", e)
        return 0, 0
