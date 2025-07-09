__version__ = "1.41.64"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2025, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/"

import logging

logging.disable(logging.WARNING)

from sys import version

from armagomen.utils.logging import logInfo
from realm import CURRENT_REALM

_mod = []


def init():
    from armagomen._constants import IS_WG_CLIENT
    from armagomen.battle_observer.core import Core
    logInfo('MOD START LOADING: v{}', __version__)
    logInfo('Launched at python v{} region={}', version, CURRENT_REALM)
    if IS_WG_CLIENT:
        from armagomen.battle_observer.core.updater import Updater
        _mod.append(Updater(__version__))
    _mod.append(Core(__version__))

    for component in _mod:
        component.start()


def fini():
    while _mod:
        _mod.pop().fini()

    logInfo('MOD SHUTTING DOWN: v{}', __version__)


onAvatarBecomePlayer = lambda: None
onAccountBecomePlayer = lambda: None
onAccountBecomeNonPlayer = lambda: None
onConnected = lambda: None
onDisconnected = lambda: None
onAccountShowGUI = lambda ctx: None
