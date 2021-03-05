from armagomen.battle_observer import init, fini
import logging

if callable(init) and callable(fini):
    logging.disable(logging.WARNING)