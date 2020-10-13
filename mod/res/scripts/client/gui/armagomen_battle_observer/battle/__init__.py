from importlib import import_module

from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI, _SPECTATOR_UI
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from ..core.battle_elements_settings_cache import g_settingsGetter
from ..core.bo_constants import GLOBAL, SWF
from ..core.bw_utils import logError, callback


def getViewSettings():
    settings = []
    for alias in g_settingsGetter.sorted_aliases:
        if g_settingsGetter.getSetting(alias):
            try:
                class_name = alias.split("_")[GLOBAL.ONE]
                file_name = g_settingsGetter.alias_to_path.get(alias)
                module_class = getattr(import_module(file_name, package=__package__), class_name)
                settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
                _GAME_UI.add(alias)
                _SPECTATOR_UI.add(alias)
            except Exception as err:
                from ..core.bw_utils import logWarning
                logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = [
            (VIEW_ALIAS.CLASSIC_BATTLE_PAGE, lambda event: callback(2.0, lambda: self.listener(event))),
            (VIEW_ALIAS.RANKED_BATTLE_PAGE, lambda event: callback(2.0, lambda: self.listener(event))),
            (VIEW_ALIAS.EPIC_RANDOM_PAGE, lambda event: callback(2.0, lambda: self.listener(event)))
        ]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def listener(self, event):
        battle_page = self._app.containerManager.getViewByKey(event.loadParams.viewKey)
        if battle_page is not None and battle_page._isDAAPIInited():
            flash = battle_page.flashObject
            for comp in g_settingsGetter.sorted_aliases:
                if g_settingsGetter.getSetting(comp):
                    if hasattr(flash, SWF.ATTRIBUTE_NAME):
                        flash.as_createBattleObserverComp(comp)
                    else:
                        to_format_str = "{}, {}, has ho attribute {}"
                        logError(to_format_str.format(comp, repr(flash), SWF.ATTRIBUTE_NAME))
