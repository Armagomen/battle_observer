from armagomen.battle_observer.settings import user_settings
from armagomen.utils.logging import logDebug
from comp7.gui.impl.lobby.hangar.comp7_hangar import Comp7HangarWindow
from comp7_light.gui.impl.lobby.hangar.comp7_light_hangar import Comp7LightHangarWindow
from frameworks.wulf.gui_constants import ShowingStatus
from gui.impl.lobby.hangar.random.random_hangar import HangarWindow
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from helpers import dependency
from last_stand.gui.impl.lobby.hangar_view import HangarWindow as LastStandWindow
from skeletons.gui.impl import IGuiLoader

SHOWING_STATUS_TO_VALUE = {ShowingStatus.SHOWN.value: True, ShowingStatus.HIDDEN.value: False}
NOT_HIDE = (HangarWindow, Comp7LightHangarWindow, Comp7HangarWindow, LastStandWindow)


class BaseModMeta(BaseDAAPIComponent):
    gui = dependency.descriptor(IGuiLoader)

    def __init__(self):
        super(BaseModMeta, self).__init__()
        self.settings = None

    def _populate(self):
        super(BaseModMeta, self)._populate()
        logDebug("hangar module '{}' loaded", self.getAlias())
        self.gui.windowsManager.onWindowShowingStatusChanged += self.onWindowShowingStatusChanged

    def _dispose(self):
        self.gui.windowsManager.onWindowShowingStatusChanged -= self.onWindowShowingStatusChanged
        logDebug("hangar module '{}' dispose", self.getAlias())
        super(BaseModMeta, self)._dispose()

    def setAlias(self, alias):
        super(BaseModMeta, self).setAlias(alias)
        self.settings = user_settings.getSettingDictByAliasLobby(alias)

    def as_startUpdateS(self, *args):
        return self.flashObject.as_startUpdate(*args) if self._isDAAPIInited() else None

    def getSettings(self):
        return self.settings

    def setVisible(self, visible):
        return self.flashObject.as_setVisible(visible) if self._isDAAPIInited() else None

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        pass
