from armagomen.battle_observer import init, fini

if callable(init) and callable(fini):
    import logging

    logging.disable(logging.WARNING)
