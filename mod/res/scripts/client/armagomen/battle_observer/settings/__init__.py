def register_settings():
    from helpers.dependency import _g_manager, DependencyManager
    from armagomen.battle_observer.settings.settings_loader import SettingsLoader
    from armagomen.battle_observer.settings.interface import IBOSettingsLoader

    manager = _g_manager  # type: DependencyManager
    manager.addInstance(IBOSettingsLoader, SettingsLoader(), finalizer='fini')
