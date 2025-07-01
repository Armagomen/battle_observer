import json
import urllib2

from armagomen.utils.logging import logError

BASE_URL = "https://battle-observer.firebaseio.com"
TOKEN = "jt0cTgfMZIYgEZNuEwjIykhTJFJkOIxNEMHxfbA6"

# MEASUREMENT_ID = "G-VLCMRH2CTP"
# API_SECRET = "H-MWk99TQgiG0h_7DeUHnQ"

def get_url(path):
    return BASE_URL + path + ".json?auth=" + TOKEN

def get_full_url():
    return BASE_URL + "/.json?auth=" + TOKEN

def is_known_user(user_id):
    try:
        url = get_url("/known_users/%s" % user_id)
        response = urllib2.urlopen(url)
        return response.read().strip() != "null"
    except Exception as e:
        logError("[Firebase] Error checking known user: {}", e)
        return False

# def log_event(event_name, user_id):
#     url = "https://www.google-analytics.com/mp/collect?measurement_id=%s&api_secret=%s" % (MEASUREMENT_ID, API_SECRET)
#
#     payload = {
#         "client_id": "wot_{}".format(user_id),
#         "events": [{
#             "name": event_name,
#             "params": {
#                 "user_id": user_id,
#                 "region": CURRENT_REALM
#             }
#         }]
#     }
#
#     try:
#         req = urllib2.Request(url, json.dumps(payload), {"Content-Type": "application/json"})
#         urllib2.urlopen(req, timeout=5)
#     except Exception as e:
#         logError("[GA4] Event '{}' logging failed: {}", event_name, e)

def user_login(user_id):
    url = get_full_url()
    payload = {
        "users/%s" % user_id: {"is_online": 1},
        "known_users/%s" % user_id: 1,
        "stats/online_count": {".sv": {"increment": 1}}
    }

    if not is_known_user(user_id):
        payload["stats/total_count"] = {".sv": {"increment": 1}}
        # log_event("new_user", user_id)

    try:
        req = urllib2.Request(url, json.dumps(payload), {"Content-Type": "application/json"})
        req.get_method = lambda: "PATCH"
        urllib2.urlopen(req)
    except Exception as e:
        logError("[Firebase] Login PATCH failed: {}", e)

    # log_event("user_login", user_id)

def user_logout(user_id):
    url = get_full_url()
    payload = {
        "users/%s/is_online" % user_id: 0,
        "stats/online_count": {".sv": {"increment": -1}}
    }

    try:
        req = urllib2.Request(url, json.dumps(payload), {"Content-Type": "application/json"})
        req.get_method = lambda: "PATCH"
        urllib2.urlopen(req)
    except Exception as e:
        logError("[Firebase] Logout PATCH failed: {}", e)

    # log_event("user_logout", user_id)

def get_stats():
    try:
        data = json.loads(urllib2.urlopen(get_url("/stats")).read())
        return data.get("online_count", 0), data.get("total_count", 0)
    except Exception as e:
        logError("[Firebase] Failed to retrieve stats: {}", e)
        return 0, 0