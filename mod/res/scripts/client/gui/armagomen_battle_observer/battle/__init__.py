from importlib import import_module

from gui.Scaleform.daapi.view.battle.epic.page import _GAME_UI
from gui.Scaleform.framework import ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE, events
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider
from ..core.battle_core import b_core
from ..core.battle_elements_settings_cache import g_settingsGetter
from ..core.bo_constants import GLOBAL, SWF


def getViewSettings():
    settings = []
    for alias in g_settingsGetter.sorted_aliases:
        if g_settingsGetter.getSetting(alias):
            try:
                class_name = alias.split("_")[GLOBAL.ONE]
                file_name = g_settingsGetter.alias_to_path.get(alias)
                module_class = getattr(import_module(file_name, package=__package__), class_name)
                settings.append(ViewSettings(alias=alias, clazz=module_class, url=None, type=ViewTypes.COMPONENT,
                                             event=None, scope=ScopeTemplates.DEFAULT_SCOPE,
                                             cacheable=False, containers=None, canDrag=False,
                                             canClose=False, isModal=False, isCentered=False))
                _GAME_UI.add(alias)
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
        self.arenaVisitor = dependency.instance(IBattleSessionProvider).arenaVisitor
        listeners = [(events.GameEvent.BATTLE_LOADING, self.listener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_BATTLE, EVENT_BUS_SCOPE.BATTLE)

    def listener(self, event):
        if event.ctx.get('isShown', False) and b_core.notEpicOrEvent(self.arenaVisitor):
            battle_page = self._app.containerManager.getContainer(ViewTypes.DEFAULT).getView()
            if battle_page._isDAAPIInited():
                flash = battle_page.flashObject
                for comp in g_settingsGetter.sorted_aliases:
                    if g_settingsGetter.getSetting(comp):
                        if hasattr(flash, SWF.ATTRIBUTE_NAME):
                            flash.as_createBattleObserverComp(comp)
                        else:
                            to_format_str = "{}, {}, has ho attribute {}"
                            from ..core.bw_utils import logError
                            logError(to_format_str.format(comp, repr(flash), SWF.ATTRIBUTE_NAME))
