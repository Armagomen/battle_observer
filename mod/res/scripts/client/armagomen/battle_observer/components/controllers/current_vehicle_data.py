from collections import namedtuple

from armagomen.utils.hangar_vehicle_getter import isSpecialVehicle
from armagomen.utils.logging import logDebug
from CurrentVehicle import g_currentVehicle
from dossiers2.ui.achievements import MARK_ON_GUN_RECORD
from Event import SafeEvent
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader
from skeletons.gui.shared import IItemsCache

PARAMS = ("tankAvgDamage", "tankAvgAssist", "tankAvgStun", "tankAvgBlocked", "marksOnGunValue", "marksOnGunIcon", "name", "marksAvailable",
          "winRate", "battles")
EfficiencyAVGData = namedtuple("EfficiencyAVGData", PARAMS)


class CurrentVehicleCachedData(object):
    __slots__ = ("__EfficiencyAVGData", "__default", "onChanged")
    itemsCache = dependency.descriptor(IItemsCache)
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.onChanged = SafeEvent()
        default = 2000
        self.__default = EfficiencyAVGData(default, default, default, 0, 0.0, "", "Undefined", False, 0.0, 0)
        self.__EfficiencyAVGData = None

        self.appLoader.onGUISpaceEntered += self.subscribe
        self.appLoader.onGUISpaceLeft += self.unsubscribe

    def subscribe(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        logDebug("CurrentVehicleCachedData::subscribe lobby")
        g_currentVehicle.onChanged += self.onVehicleChanged

    def unsubscribe(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        logDebug("CurrentVehicleCachedData::unsubscribe lobby")
        g_currentVehicle.onChanged -= self.onVehicleChanged

    def onVehicleChanged(self):
        self.__EfficiencyAVGData = self.setAvgData() if g_currentVehicle.isPresent() and not isSpecialVehicle(
            g_currentVehicle.item) else None
        self.onChanged(self.__EfficiencyAVGData)

    def setAvgData(self):
        dossier = self.itemsCache.items.getVehicleDossier(g_currentVehicle.intCD)
        random = dossier.getRandomStats()
        marks = random.getAchievement(MARK_ON_GUN_RECORD)
        blocked = random.getAvgDamageBlocked() or 0
        return EfficiencyAVGData(
            int(random.getAvgDamage() or 0),
            int(random.getDamageAssistedEfficiency() or 0),
            int(random.getAvgDamageAssistedStun() or 0),
            int(blocked) if blocked > 99 else round(blocked, 2),
            marks.getDamageRating(),
            "<img src='img://gui/{}' width='20' height='18' vspace='-8'>".format(marks.getIcons()[marks.IT_95X85][3:]),
            g_currentVehicle.item.userName,
            g_currentVehicle.item.level > 4,
            (random.getWinsEfficiency() or 0.0) * 100,
            int(random.getBattlesCount())
        )

    @property
    def efficiencyAvgData(self):
        return self.__EfficiencyAVGData or self.__default

    @property
    def default(self):
        return self.__default

    def fini(self):
        self.appLoader.onGUISpaceEntered -= self.subscribe
        self.appLoader.onGUISpaceLeft -= self.unsubscribe
