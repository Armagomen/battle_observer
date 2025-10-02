__version__ = "1.43.07"
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
    if CURRENT_REALM == "RU":
        return
    from armagomen.battle_observer.core import Core
    logInfo('MOD START LOADING: v{}', __version__)
    logInfo('Launched at python v{} region={}', version, CURRENT_REALM)
    from armagomen.battle_observer.core.updater import Updater
    _mod.append(Updater(__version__))
    _mod.append(Core(__version__))

    for component in _mod:
        component.start()


def fini():
    if CURRENT_REALM == "RU":
        return
    while _mod:
        _mod.pop().fini()

    logInfo('MOD SHUTTING DOWN: v{}', __version__)


onAvatarBecomePlayer = lambda *a, **kw: None
onAccountBecomePlayer = lambda *a, **kw: None
onAccountBecomeNonPlayer = lambda *a, **kw: None
onConnected = lambda *a, **kw: None
onDisconnected = lambda *a, **kw: None
onAccountShowGUI = lambda *a, **kw: None
