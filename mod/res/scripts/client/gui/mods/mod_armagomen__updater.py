from debug_utils import LOG_CURRENT_EXCEPTION

try:
    from armagomen.battle_observer.core import __version__
    from armagomen.battle_observer.core.updater import Updater

    Updater(__version__)
except Exception:
    LOG_CURRENT_EXCEPTION()
