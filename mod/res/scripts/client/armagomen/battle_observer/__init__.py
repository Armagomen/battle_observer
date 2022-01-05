__author__ = "Armagomen"
__version__ = "1.36.5"
__copyright__ = "Copyright 2014-2022, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__maintainer__ = "Armagomen"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "localhost"
__all__ = ['init', 'fini', 'onConnected', 'onDisconnected']

from armagomen.battle_observer.core import init, fini
from armagomen.utils.events import g_events


def onConnected(*args, **kwargs):
    g_events.onConnected()


def onDisconnected(*args, **kwargs):
    g_events.onDisconnected()
