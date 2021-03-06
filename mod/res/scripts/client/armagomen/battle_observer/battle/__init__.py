from importlib import import_module

from armagomen.battle_observer.core import v_settings
from armagomen.battle_observer.core.constants import GLOBAL, SWF, ALIAS_TO_PATH, SORTED_ALIASES
from armagomen.utils.common import logError, callback, logWarning
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def getViewSettings():
    settings = []
    for alias in SORTED_ALIASES:
        if v_settings.getSetting(alias):
            try:
                class_name = alias.split("_")[GLOBAL.ONE]
                file_name = ALIAS_TO_PATH.get(alias)
                module_class = getattr(import_module(file_name, package=__package__), class_name)
                settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
                _GAME_UI.add(alias)
                _SPECTATOR_UI.add(alias)
            except Exception as err:
                logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = [
            (VIEW_ALIAS.CLASSIC_BATTLE_PAGE, self.callbackListener),
            (VIEW_ALIAS.RANKED_BATTLE_PAGE, self.callbackListener),
            (VIEW_ALIAS.EPIC_RANDOM_PAGE, self.callbackListener)
        ]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def callbackListener(self, event):
        callback(1.5, lambda: self.eventListener(event))

    def eventListener(self, event):
        battle_page = self._app.containerManager.getViewByKey(event.loadParams.viewKey)
        if battle_page is not None and battle_page._isDAAPIInited():
            flash = battle_page.flashObject
            if hasattr(flash, SWF.ATTRIBUTE_NAME):
                for comp in SORTED_ALIASES:
                    if v_settings.getSetting(comp):
                        flash.as_createBattleObserverComp(comp)
            else:
                to_format_str = "battle_page {}, has ho attribute {}"
                logError(to_format_str.format(repr(flash), SWF.ATTRIBUTE_NAME))
        else:
            callback(1.0, lambda: self.eventListener(event))
