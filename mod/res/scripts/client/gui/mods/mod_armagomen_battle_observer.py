__version__ = "1.40.08"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2022, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

import logging

from armagomen.battle_observer.core import onInit, onFini
from helpers.statistics import StatisticsCollector

logging.disable(logging.ERROR)
StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None


def init():
    onInit(__version__)


def fini():
    onFini(__version__)
