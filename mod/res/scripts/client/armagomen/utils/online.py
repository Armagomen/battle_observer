import json
import urllib2

BASE_URL = "https://battle-observer.firebaseio.com"
TOKEN = "jt0cTgfMZIYgEZNuEwjIykhTJFJkOIxNEMHxfbA6"


def get_url(path):
    return BASE_URL + path + ".json?auth=" + TOKEN


def user_exists_and_online(user_id):
    url = get_url("/users/%s" % user_id)
    try:
        data = json.loads(urllib2.urlopen(url).read())
        return data and data.get("is_online") == True
    except:
        return False


def is_known_user(user_id):
    url = get_url("/known_users/%s" % user_id)
    try:
        result = json.loads(urllib2.urlopen(url).read())
        return result == True
    except:
        return False


def mark_user_as_known(user_id):
    url = get_url("/known_users/%s" % user_id)
    data = json.dumps(True)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    req.get_method = lambda: 'PUT'
    urllib2.urlopen(req)


def increment_stat(counter, value):
    url = get_url("/stats/%s" % counter)
    data = json.dumps({".sv": {"increment": value}})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    req.get_method = lambda: 'PUT'
    urllib2.urlopen(req)


def user_login(user_id):
    if user_exists_and_online(user_id):
        return
    is_new = not is_known_user(user_id)
    url = get_url("/users/%s" % user_id)
    data = json.dumps({"is_online": True})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    req.get_method = lambda: 'PUT'
    urllib2.urlopen(req)
    increment_stat("online_count", 1)
    if is_new:
        increment_stat("total_count", 1)
        mark_user_as_known(user_id)


def user_logout(user_id):
    if not user_exists_and_online(user_id):
        return
    url = get_url("/users/%s" % user_id)
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE'
    urllib2.urlopen(req)
    increment_stat("online_count", -1)


def get_stats():
    try:
        url = get_url("/stats")
        data = json.loads(urllib2.urlopen(url).read())
        online = data.get("online_count", 0)
        total = data.get("total_count", 0)
        return online, total
    except:
        return 0, 0
