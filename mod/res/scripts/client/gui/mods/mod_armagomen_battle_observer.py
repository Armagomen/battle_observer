__version__ = "1.41.63"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2025, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/releases"

import logging

logging.disable(logging.WARNING)

from sys import version

from armagomen.utils.logging import logInfo
from realm import CURRENT_REALM

__mod = []


def init():
    from armagomen._constants import IS_WG_CLIENT
    from armagomen.battle_observer.core import Core
    logInfo('MOD START LOADING: v{}', __version__)
    logInfo('Launched at python v{} region={}', version, CURRENT_REALM)
    if IS_WG_CLIENT:
        from armagomen.battle_observer.core.updater import Updater
        __mod.append(Updater(__version__))
    __mod.append(Core(__version__))

    for component in __mod:
        component.start()


def fini():
    for component in __mod:
        component.fini()

    logInfo('MOD SHUTTING DOWN: v{}', __version__)
