__version__ = "1.43.46"
__author__ = "Armagomen"
__copyright__ = "Copyright 2014-2026, Armagomen"
__license__ = "CC BY-NC-SA 4.0"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "https://github.com/Armagomen/battle_observer/"
__name__ = "BATTLE_OBSERVER"

import logging

loggers = (
    "Account",
    "Avatar",
    "AvatarInputHandler.kill_cam_modes",
    "BattleReplay",
    "ClientArena",
    "HWArenaPhasesComponent",
    "OwnVehicle",
    "Vehicle",
    "WebBrowser",
    "account_helpers.dog_tags",
    "arena_vscript_config.config",
    "cgf_components.arena_camera_manager",
    "cgf_components.hangar_camera_manager",
    "dyn_objects_cache",
    "frameworks.wulf.windows_system.window",
    "gui.anonymizer.contacts_uploader",
    "gui.subhangar.subhangar_observer",
    "gui.app_loader.loader",
    "gui.battle_control.arena_info.arena_dp",
    "gui.battle_results.service",
    "gui.game_control.BrowserController",
    "gui.game_control.trade_in",
    "gui.game_control.wallet",
    "gui.game_control.wot_plus.service_record_customization.service_record_customization",
    "gui.impl.backport.backport_r",
    "gui.impl.pub.fullscreen_manager",
    "gui.impl.pub.notification_window_controller",
    "gui.lobby_state_machine.lobby_state_machine",
    "gui.lobby_state_machine.states",
    "gui.prb_control.entities.base.pre_queue.vehicles_watcher",
    "gui.shared.gui_items.vehicle_equipment",
    "gui.shared.personality",
    "helpers.server_settings",
    "helpers.tips",
    "helpers.web.app_storage",
    "hints_common.prebattle.manager",
    "web.cache.web_cache",
)

for name in loggers:
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)


def init():
    from realm import CURRENT_REALM
    if CURRENT_REALM == "RU":
        return
    from helpers.dependency import _g_manager, DependencyManager

    manager = _g_manager  # type: DependencyManager
    from armagomen._logger.ALogger import ALogger, IALogger
    manager.addInstance(IALogger, ALogger(logging.getLogger(__name__)), finalizer='fini')

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
