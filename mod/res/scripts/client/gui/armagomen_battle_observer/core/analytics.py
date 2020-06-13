import sys
import threading
import urllib
import urllib2

from constants import AUTH_REALM
from debug_utils import LOG_CURRENT_EXCEPTION
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from .bo_constants import MOD_NAME, MOD_VERSION
from .bw_utils import logWarning
from .config import c_Loader


def cleanupNetwork():
    modules = ['socket', 'httplib', 'urllib2', 'urllib']
    for module in modules:
        if module in sys.modules:
            if module in globals():
                del sys.modules[module]
                globals()[module] = __import__(module)


class Analytics(object):
    __slots__ = ('user',)

    def __init__(self):
        self.user = None
        ServicesLocator.connectionMgr.onLoggedOn += self.start
        ServicesLocator.connectionMgr.onDisconnected += self.end

    def start(self, data):
        if self.user is None and 'token2' in data:
            self.user = data['token2'].split(':')[0]
            thread = threading.Thread(target=self.trySendStat('start', 'screenview'))
            thread.start()
            thread.join()

    def end(self):
        if self.user is not None:
            thread = threading.Thread(target=self.trySendStat('end', 'event'))
            thread.start()
            thread.join()

    @staticmethod
    def send(url, data, headers):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPRedirectHandler())
        opener.addheaders = headers.items()
        response = opener.open(url, data=data)
        response.close()

    def trySendStat(self, param, event):
        lang = getClientLanguage().upper()
        params = {
            'sc': param,
            'v': 1,
            'tid': 'UA-81349715-2',
            'cid': self.user,
            't': event,
            'an': MOD_NAME,
            'av': MOD_VERSION,
            'aid': c_Loader.cName,
            'cd': 'Cluster: [{}-{}]'.format(AUTH_REALM, lang),
            'ul': lang
        }
        if event == 'event':
            params.update({'ec': event, 'ea': 'disconnect'})
        data = urllib.urlencode(params)
        headers = {'User-Agent': '{}/{}'.format(MOD_NAME, MOD_VERSION)}
        try:
            self.send('http://www.google-analytics.com/collect', data, headers)
        except Exception as err:
            logWarning("Unable to send data analytics, {}".format(repr(err)))
            cleanupNetwork()
            try:
                self.send('http://www.google-analytics.com/collect', data, headers)
            except Exception as err:
                logWarning("Unable to send data analytics, {}".format(repr(err)))
                LOG_CURRENT_EXCEPTION()
        if param == 'end':
            self.user = None


analytics = Analytics()
