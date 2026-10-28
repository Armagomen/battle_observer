from armagomen._logger import IALogger
from armagomen.battle_observer.hangar_gf.date_times import DateTimesView
from armagomen.battle_observer.hangar_gf.efficiency import HangarEfficiencyView
from armagomen.battle_observer.hangar_gf.haeder import HeaderView
from armagomen.utils.common import safe_import, toggleOverride
from gui.impl.lobby.page.lobby_header import LobbyHeader
from helpers import dependency
from skeletons.gui.game_control import IHangarGuiController


class HangarGamefaceInject(object):
    logger = dependency.descriptor(IALogger)
    _hangarGuiCtrl = dependency.descriptor(IHangarGuiController)

    headers = safe_import((
        ("comp7.gui.impl.lobby.page.lobby_header", "Comp7LobbyHeader"),
        ("comp7_light.gui.impl.lobby.page.lobby_header", "Comp7LightLobbyHeader"),
        ("last_stand.gui.impl.lobby.page.ls_lobby_header", "LSLobbyHeader"),
        ("fort_rush.gui.impl.lobby.page.example_lobby_header", "ExampleLobbyHeader")
    ))

    def _getViewType(self):
        controlsHelper = self._hangarGuiCtrl.currentGuiProvider.getLobbyHeaderHelper()
        return controlsHelper.getHeaderType() if controlsHelper is not None else None

    def __init__(self):
        toggleOverride(LobbyHeader, '_initChildren', self.hooked_initChildren, True)

    def fini(self):
        toggleOverride(LobbyHeader, '_initChildren', self.hooked_initChildren, False)

    def _registerChild(self, child, baseView):
        try:
            baseView._registerChild(child.viewLayoutID(), child())
        except Exception as error:
            self.logger.logError(error)

    def hooked_initChildren(self, baseMethod, baseView):
        baseMethod(baseView)
        self._registerChild(DateTimesView, baseView)
        self._registerChild(HeaderView, baseView)
        if self.headers and isinstance(baseView, self.headers):
            return
        self._registerChild(HangarEfficiencyView, baseView)
