from armagomen.utils.common import urlResponse

response = urlResponse("http://ipinfo.io/json")
if response and 'RU' not in response['country']:
    import logging

    from armagomen.battle_observer import init, fini, onConnected, onDisconnected
    from helpers.statistics import StatisticsCollector

    if callable(init) and callable(fini):
        logging.disable(logging.ERROR)

    StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None
