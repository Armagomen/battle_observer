__all__ = ['init', 'fini', 'onConnected', 'onDisconnected']

from armagomen.battle_observer.core import init, fini
from armagomen.utils.events import g_events


def onConnected(*args, **kwargs):
    g_events.onConnected()


def onDisconnected(*args, **kwargs):
    g_events.onDisconnected()
