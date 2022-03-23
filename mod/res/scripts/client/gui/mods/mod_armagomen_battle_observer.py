import locale

if locale.getdefaultlocale()[0] not in ("ba_RU", "ru_RU", "tt_RU", "sah_RU"):
    import logging

    from armagomen.battle_observer import init, fini
    from helpers.statistics import StatisticsCollector

    if callable(init) and callable(fini):
        logging.disable(logging.ERROR)

    StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None
