from armagomen.utils.common import delayedCall
from CurrentVehicle import g_currentVehicle
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader

flags = ('isOnlyForFunRandomBattles', 'isOnlyForBattleRoyaleBattles', 'isOnlyForMapsTrainingBattles',
         'isOnlyForClanWarsBattles', 'isOnlyForComp7Battles', 'isOnlyForEventBattles', 'isOnlyForEpicBattles')


def isSpecialBattleVehicle(vehicle):
    return vehicle is None or any(getattr(vehicle, f, False) for f in flags)


class OnVehicleChangeSubscribed(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.appLoader.onGUISpaceBeforeEnter += self.__onGUISpaceBeforeEnter
        self.appLoader.onGUISpaceLeft += self.__onGUISpaceLeft

    def fini(self):
        self.appLoader.onGUISpaceBeforeEnter -= self.__onGUISpaceBeforeEnter
        self.appLoader.onGUISpaceLeft -= self.__onGUISpaceLeft

    def __onGUISpaceBeforeEnter(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        g_currentVehicle.onChanged += self.__onChanged

    def __onGUISpaceLeft(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        g_currentVehicle.onChanged -= self.__onChanged

    @delayedCall(0.1)
    def __onChanged(self):
        vehicle = g_currentVehicle.item
        self.onVehicleChanged(None if isSpecialBattleVehicle(vehicle) else vehicle)

    def onVehicleChanged(self, vehicle):
        raise NotImplementedError
