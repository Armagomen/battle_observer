import locale

locations = (
    locale.windows_locale[0x046d],  # Bashkir ba_RU
    locale.windows_locale[0x0419],  # Russian ru_RU
    locale.windows_locale[0x0444],  # Tatar tt_RU
    locale.windows_locale[0x0485]   # Yakut - Cyrillic sah_RU
)

if locale.getdefaultlocale()[0] not in locations:
    import logging

    from armagomen.battle_observer import init, fini
    from helpers.statistics import StatisticsCollector

    if callable(init) and callable(fini):
        logging.disable(logging.ERROR)

    StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None
