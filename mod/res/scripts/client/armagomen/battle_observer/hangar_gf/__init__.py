from armagomen.utils.logging import logError
from openwg_gameface import manager

from armagomen.battle_observer.hangar_gf.date_times import DateTimesView
from armagomen.battle_observer.hangar_gf.efficiency import HangarEfficiencyView
from armagomen.battle_observer.hangar_gf.haeder import HeaderView
from armagomen.utils.common import overrideMethod
from comp7.gui.impl.lobby.page.lobby_header import Comp7LobbyHeader
from comp7_light.gui.impl.lobby.page.lobby_header import Comp7LightLobbyHeader
from gui.impl.lobby.page.lobby_header import LobbyHeader



class HangarGamefaceInject(object):

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
        if isinstance(baseView, (Comp7LobbyHeader, Comp7LightLobbyHeader)):
            return
        self._registerChild(HangarEfficiencyView, baseView)
