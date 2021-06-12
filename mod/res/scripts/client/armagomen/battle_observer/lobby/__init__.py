from importlib import import_module

from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, CLOCK, SWF
from armagomen.utils.common import logError, callback, logWarning
from frameworks.wulf import WindowLayer
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ComponentSettings, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE


def getComponents():
    return (
        ('Observer_DateTimes_UI',
         settings.clock[GLOBAL.ENABLED] and settings.clock[CLOCK.IN_LOBBY][GLOBAL.ENABLED]),
    )


def getViewSettings():
    settings = []
    for alias, enable in getComponents():
        try:
            class_name = alias.split("_")[1]
            module_class = getattr(import_module(".date_times", package=__package__), class_name)
            settings.append(ComponentSettings(alias, module_class, ScopeTemplates.DEFAULT_SCOPE))
        except Exception as err:
            logWarning("{}, {}, {}".format(__package__, alias, repr(err)))
    return settings


def getBusinessHandlers():
    return ObserverBusinessHandler(),


def getContextMenuHandlers():
    return ()


class ObserverBusinessHandler(PackageBusinessHandler):
    __slots__ = ()

    def __init__(self):
        listeners = [(VIEW_ALIAS.LOBBY_HANGAR, self.callbackListener)]
        super(ObserverBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def callbackListener(self, event):
        self._app.as_loadLibrariesS([SWF.LOBBY])
        callback(1.0, lambda: self.eventListener(event))

    def eventListener(self, event):
        if event.name == VIEW_ALIAS.LOBBY_HANGAR:
            lobby_page = self._app.containerManager.getContainer(WindowLayer.VIEW).getView()
            if lobby_page is not None and lobby_page._isDAAPIInited():
                flash = lobby_page.flashObject
                if hasattr(flash, SWF.ATTRIBUTE_NAME):
                    for comp, enabled in getComponents():
                        if enabled and not lobby_page.isFlashComponentRegistered(comp):
                            flash.as_createBattleObserverComp(comp)
                else:
                    to_format_str = "lobby_page {}, has ho attribute {}"
                    logError(to_format_str.format(repr(flash), SWF.ATTRIBUTE_NAME))
            else:
                callback(0.2, lambda: self.eventListener(event))
