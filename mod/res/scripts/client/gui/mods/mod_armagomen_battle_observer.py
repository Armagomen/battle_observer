__version__ = "1.41.21"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2024, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

from threading import Thread

from armagomen.battle_observer.core import Core, onFini
from helpers.statistics import StatisticsCollector

StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None

observer = Thread(target=Core, args=(__version__,), name="Battle_Observer")


def init():
    observer.start()


def fini():
    observer.join()
    onFini(__version__)
