__version__ = "1.43.32"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2026, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/"
__name__ = "BATTLE_OBSERVER"

import logging

logging.disable(logging.WARNING)

from realm import CURRENT_REALM
from armagomen import IALogger


def init():
    if CURRENT_REALM == "RU":
        return
    from helpers.dependency import _g_manager, DependencyManager
    from sys import version

    manager = _g_manager  # type: DependencyManager
    logger = manager.getService(IALogger)
    logger.logInfo('MOD START LOADING: v{}', __version__)
    logger.logInfo('Launched at python v{} region={}', version, CURRENT_REALM)

    from armagomen.battle_observer import Core, IBOCore
    from armagomen.battle_observer.updater import Updater, IBOUpdater
    services = ((IBOCore, Core), (IBOUpdater, Updater))

    for interface, service in services:
        manager.addInstance(interface, service(__version__), finalizer='fini')


fini = lambda *a, **kw: None
onAvatarBecomePlayer = lambda *a, **kw: None
onAccountBecomePlayer = lambda *a, **kw: None
onAccountBecomeNonPlayer = lambda *a, **kw: None
onConnected = lambda *a, **kw: None
onDisconnected = lambda *a, **kw: None
onAccountShowGUI = lambda *a, **kw: None
