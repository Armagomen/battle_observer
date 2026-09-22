__version__ = "1.43.44"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2026, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/"
__name__ = "BATTLE_OBSERVER"

import logging

logging.disable(logging.DEBUG)


def init():
    from realm import CURRENT_REALM
    if CURRENT_REALM == "RU":
        return
    from helpers.dependency import _g_manager, DependencyManager

    manager = _g_manager  # type: DependencyManager
    from armagomen._logger import IALogger
    from armagomen._logger.ALogger import ALogger

    manager.addInstance(IALogger, ALogger(__name__), finalizer='fini')

    from armagomen.battle_observer import Core, IBOCore
    from armagomen.battle_observer.updater import Updater, IBOUpdater

    manager.addInstance(IBOCore, Core(__version__), finalizer='fini')
    manager.addInstance(IBOUpdater, Updater(__version__), finalizer='fini')


fini = lambda *a, **kw: None
onAvatarBecomePlayer = lambda *a, **kw: None
onAccountBecomePlayer = lambda *a, **kw: None
onAccountBecomeNonPlayer = lambda *a, **kw: None
onConnected = lambda *a, **kw: None
onDisconnected = lambda *a, **kw: None
onAccountShowGUI = lambda *a, **kw: None
