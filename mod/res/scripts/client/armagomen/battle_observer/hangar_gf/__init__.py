from armagomen.battle_observer.hangar_gf.date_times import DateTimesView
from armagomen.battle_observer.hangar_gf.efficiency import HangarEfficiencyView
from armagomen.battle_observer.hangar_gf.haeder import HeaderView
from armagomen.utils.common import overrideMethod, safe_import
from armagomen.utils.logging import logError
from gui.impl.lobby.page.lobby_header import LobbyHeader
from openwg_gameface import manager


class HangarGamefaceInject(object):
    headers = safe_import((
        ("comp7.gui.impl.lobby.page.lobby_header", "Comp7LobbyHeader"),
        ("comp7_light.gui.impl.lobby.page.lobby_header", "Comp7LightLobbyHeader"),
        ("last_stand.gui.impl.lobby.page.ls_lobby_header", "LSLobbyHeader")
    ))

    def __init__(self):
        overrideMethod(LobbyHeader, '_initChildren')(self.hooked_initChildren)

    @staticmethod
    def _registerChild(child, baseView):
        try:
            baseView._registerChild(child.viewLayoutID(), child())
        except Exception as error:
            logError(repr(error))

    def hooked_initChildren(self, baseMethod, baseView):
        baseMethod(baseView)
        if not manager.isResMapValidated:
            return
        self._registerChild(DateTimesView, baseView)
        self._registerChild(HeaderView, baseView)
        if self.headers and isinstance(baseView, self.headers):
            return
        self._registerChild(HangarEfficiencyView, baseView)
