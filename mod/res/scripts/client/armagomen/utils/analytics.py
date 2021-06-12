import urllib2

from armagomen.constants import URLS, HEADERS
from armagomen.utils.common import logWarning
from async import async, await, AsyncReturn
from gui.shared.personality import ServicesLocator


class Analytics(object):
    __slots__ = ('user', 'url')

    def __init__(self):
        self.user = None
        self.url = 'http://{}/api/v1/online_counter/?method={}&databaseID={}'
        ServicesLocator.connectionMgr.onLoggedOn += self.start
        ServicesLocator.connectionMgr.onDisconnected += self.end

    @async
    def start(self, data):
        if self.user is None and 'token2' in data:
            self.user = data['token2'].split(':')[0]
            yield await(self.send_data('login', self.user))

    @async
    def end(self):
        if self.user is not None:
            yield await(self.send_data('logout', self.user))

    @async
    def send_data(self, method, databaseID):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
            opener.addheaders = HEADERS
            opener.open(self.url.format(URLS.HOST_NAME, method, databaseID))
            opener.close()
        except urllib2.URLError:
            logWarning("Technical problems with the server, please inform the developer.")
        if method == 'logout':
            self.user = None
        raise AsyncReturn(True)


analytics = Analytics()
