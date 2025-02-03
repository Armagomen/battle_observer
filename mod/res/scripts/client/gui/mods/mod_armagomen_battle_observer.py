__version__ = "1.41.39"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2024, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

import logging

logging.disable(logging.WARNING)

from sys import version
from threading import Thread

from armagomen.battle_observer.core import Core, onFini
from armagomen.battle_observer.core.updater import Updater
from armagomen.utils.logging import logInfo
from realm import CURRENT_REALM

__update = Thread(target=Updater, args=(__version__,), name="Battle_Observer_update")
__observer = Thread(target=Core, args=(__version__, Thread), name="Battle_Observer_Core")


def init():
    logInfo('MOD START LOADING: v{}', __version__)
    logInfo('Launched at python v{} region={}', version, CURRENT_REALM)
    __update.start()
    __observer.start()


def fini():
    __observer.join()
    __update.join()
    onFini()
    logInfo('MOD SHUTTING DOWN: v{}', __version__)
