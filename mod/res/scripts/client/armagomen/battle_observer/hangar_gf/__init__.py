def addHooks():
    from openwg_gameface import manager

    from armagomen.battle_observer.hangar_gf.date_times import DateTimesView
    from armagomen.battle_observer.hangar_gf.hangar_efficiency import HangarEfficiencyView
    from armagomen.utils.common import overrideMethod
    from comp7.gui.impl.lobby.page.lobby_header import Comp7LobbyHeader
    from comp7_light.gui.impl.lobby.page.lobby_header import Comp7LightLobbyHeader
    from gui.impl.lobby.page.lobby_header import LobbyHeader

    @overrideMethod(LobbyHeader, '_initChildren')
    @overrideMethod(Comp7LightLobbyHeader, '_initChildren')
    @overrideMethod(Comp7LobbyHeader, '_initChildren')
    def hooked_initChildren(baseMethod, baseObject):
        baseMethod(baseObject)
        if not manager.isResMapValidated:
            return
        baseObject.setChildView(DateTimesView.viewLayoutID(), DateTimesView())
        baseObject.setChildView(HangarEfficiencyView.viewLayoutID(), HangarEfficiencyView())
