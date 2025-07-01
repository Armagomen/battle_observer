import json
import urllib2

BASE_URL = "https://battle-observer.firebaseio.com"
TOKEN = "jt0cTgfMZIYgEZNuEwjIykhTJFJkOIxNEMHxfbA6"

def get_url(path):
    return BASE_URL + path + ".json?auth=" + TOKEN

def get_full_url():
    return BASE_URL + ".json?auth=" + TOKEN

def is_known_user(user_id):
    url = get_url("/known_users/%s" % user_id)
    try:
        result = json.loads(urllib2.urlopen(url).read())
        return result == 1 if type(result) == int else result == True
    except:
        return False

def user_login(user_id):
    url = get_full_url()
    payload = {
        "users/%s" % user_id: {"is_online": 1},
        "known_users/%s" % user_id: 1,
        "stats/online_count": {".sv": {"increment": 1}}
    }
    if not is_known_user(user_id):
        payload["stats/total_count"] = {".sv": {"increment": 1}}
    data = json.dumps(payload)
    try:
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        req.get_method = lambda: 'PATCH'
        urllib2.urlopen(req)
    except:
        pass

def user_logout(user_id):
    url = get_full_url()
    payload = {
        "users/%s/is_online" % user_id: 0,
        "stats/online_count": {".sv": {"increment": -1}}
    }
    data = json.dumps(payload)
    try:
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        req.get_method = lambda: 'PATCH'
        urllib2.urlopen(req)
    except:
        pass

def get_stats():
    try:
        url = get_url("/stats")
        data = json.loads(urllib2.urlopen(url).read())
        online = data.get("online_count", 0)
        total = data.get("total_count", 0)
        return online, total
    except:
        return 0, 0