import logging

from armagomen.battle_observer import init, fini, onConnected, onDisconnected

if callable(init) and callable(fini):
    logging.disable(logging.ERROR)
