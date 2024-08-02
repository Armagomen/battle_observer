__version__ = "1.41.20"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2024, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

from armagomen.battle_observer.core import onFini, onInit
from helpers.statistics import StatisticsCollector
from realm import CURRENT_REALM

StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None


def init():
    onInit(__version__, CURRENT_REALM)


def fini():
    onFini(__version__)
