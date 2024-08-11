__version__ = "1.41.23"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2024, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

from threading import Thread

from armagomen.battle_observer.core import Core, onFini
from armagomen.battle_observer.core.updater import Updater
from helpers.statistics import StatisticsCollector

StatisticsCollector.noteHangarLoadingState = lambda *args, **kwargs: None

__update = Thread(target=Updater, args=(__version__,), name="Battle_Observer_update")
__update.start()
__update.join(timeout=60.0)

observer = Thread(target=Core, args=(__version__,), name="Battle_Observer_Core")


def init():
    observer.start()


def fini():
    observer.join()
    onFini(__version__)
