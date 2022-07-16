__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2022, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__maintainer__ = "Armagomen"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://donatua.com/@armagomen"

import logging

from armagomen.battle_observer import init, fini
from helpers.statistics import StatisticsCollector

if callable(init) and callable(fini):
    logging.disable(logging.ERROR)

StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None
