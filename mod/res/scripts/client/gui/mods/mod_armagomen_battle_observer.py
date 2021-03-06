import logging

from armagomen.battle_observer import init, fini

if callable(init) and callable(fini):
    logging.disable(logging.WARNING)
