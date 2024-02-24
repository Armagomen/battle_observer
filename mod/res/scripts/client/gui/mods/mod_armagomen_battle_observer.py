__version__ = "1.41.07"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2024, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

from realm import CURRENT_REALM

if CURRENT_REALM != "RU":
    from armagomen.battle_observer.core import onInit, onFini
    from helpers.statistics import StatisticsCollector

    StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None


    def init():
        onInit(__version__, CURRENT_REALM)


    def fini():
        onFini(__version__)
