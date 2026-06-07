from armagomen.battle_observer.settings.settings_loader import IBOSettingsLoader

__all__ = ['IBOSettingsLoader']


def register_settings():
    from helpers.dependency import _g_manager, DependencyManager
    from armagomen.battle_observer.settings.settings_loader import SettingsLoader

    from .loading_error import ErrorMessages
    from .settings_data import SettingsData

    manager = _g_manager  # type: DependencyManager
    manager.addInstance(IBOSettingsLoader, SettingsLoader(SettingsData(), ErrorMessages()), finalizer='fini')


inited = False
if not inited:
    register_settings()
    inited = True
