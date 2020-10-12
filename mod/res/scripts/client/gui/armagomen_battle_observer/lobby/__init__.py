from importlib import import_module
import BigWorld
from frameworks.wulf import WindowLayer
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from ..core.bo_constants import GLOBAL, CLOCK, SWF
from ..core.config import cfg


def getComponents():
    return (
        ('Observer_DateTimes_UI', cfg.clock[GLOBAL.ENABLED] and cfg.clock[CLOCK.IN_LOBBY][GLOBAL.ENABLED]),
    )


def getViewSettings():
    settings = []
    for alias, enable in getComponents():
        try:
            class_name = alias.split("_")[1]
            module_class = getattr(import_module(".date_times", package=__package__), class_name)
            settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
        except Exception as err:
            from ..core.bw_utils import logWarning
            logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ()

    def __init__(self):
        listeners = [(VIEW_ALIAS.LOBBY_HANGAR, self.listener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def listener(self, event):
        if event.name == VIEW_ALIAS.LOBBY_HANGAR:
            lobby_page = self._app.containerManager.getContainer(WindowLayer.VIEW).getView()
            if lobby_page is None:
                BigWorld.callback(1.0, lambda: self.listener(event))
            if not lobby_page._isDAAPIInited():
                BigWorld.callback(1.0, lambda: self.listener(event))
            else:
                flash = lobby_page.flashObject
                for comp, enabled in getComponents():
                    if enabled and not lobby_page.isFlashComponentRegistered(comp):
                        if hasattr(flash, SWF.ATTRIBUTE_NAME):
                            flash.as_createBattleObserverComp(comp)
                        else:
                            to_format_str = "{}, {}, has ho attribute {}"
                            from ..core.bw_utils import logError
                            logError(to_format_str.format(comp, repr(flash), SWF.ATTRIBUTE_NAME))
