from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta
from armagomen.utils.common import hexToInt
from constants import ARENA_PERIOD
from gui.shared import EVENT_BUS_SCOPE, events


class ColoredIcons(BaseModMeta):

    def _populate(self):
        super(ColoredIcons, self)._populate()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange += self.onPeriodChange
            arena.onVehicleKilled += self.onVehicleKilled
        self.addListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.onNextStateSwitched, scope=EVENT_BUS_SCOPE.BATTLE)

    def _dispose(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onPeriodChange -= self.onPeriodChange
            arena.onVehicleKilled -= self.onVehicleKilled
        self.removeListener(events.GameEvent.NEXT_PLAYERS_PANEL_MODE, self.onNextStateSwitched, scope=EVENT_BUS_SCOPE.BATTLE)
        super(ColoredIcons, self)._dispose()

    def onPeriodChange(self, period, *_, **__):
        if period == ARENA_PERIOD.BATTLE and self.isComp7Battle():
            if self._isDAAPIInited():
                self.flashObject.updateAllIcons()

    def onVehicleKilled(self, vehicleID, *args):
        if self._isDAAPIInited():
            self.flashObject.as_on_killed(vehicleID)

    def getConvertedColors(self):
        return {name: hexToInt(color) for name, color in self.settings.iteritems() if
                isinstance(color, basestring) and color.startswith("#")}

    def onNextStateSwitched(self, *args):
        if self._isDAAPIInited():
            self.flashObject.as_updatePositions()
