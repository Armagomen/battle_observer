from armagomen.utils.common import overrideMethod
from armagomen.utils.logging import logInfo
from gui.impl.gen.view_models.common.battle_player import BattlePlayer

__items = {}

@overrideMethod(BattlePlayer, "setVehicleId")
def setVehicleId(base, player, value):
    base(player, value)
    __items[value] = player


from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID

def onGUISpaceEntered(spaceID):
    if spaceID == GuiGlobalSpaceID.LOBBY:
        __items.clear()
    elif spaceID == GuiGlobalSpaceID.BATTLE:
        for player in __items.values():
            player.setUserName("<font color='#FFFF00'>TEST</font>")
            logInfo(dir(player.proxy))

ServicesLocator.appLoader.onGUISpaceEntered += onGUISpaceEntered


def getTabItems():
    return __items