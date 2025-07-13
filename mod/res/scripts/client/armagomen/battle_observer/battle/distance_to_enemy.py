# coding=utf-8
from armagomen._constants import GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.utils.common import getPlayer
from gui.battle_control.avatar_getter import getDistanceToTarget, getInputHandler
from gui.battle_control.battle_constants import PLAYER_GUI_PROPS
from helpers import getClientLanguage


class Distance(DistanceMeta):

    def __init__(self):
        super(Distance, self).__init__()
        self.isPostmortem = False
        self.vehicles = {}
        self.player = None
        if getClientLanguage() in ('uk', 'ru', 'be'):
            self.__tpl = "<font color='{}' size='{}'>%.1f до %s</font>"
        else:
            self.__tpl = "<font color='{}' size='{}'>%.1f to %s</font>"
        self.template = self.__tpl.format("#f5ff8f", 18)

    def _populate(self):
        super(Distance, self)._populate()
        self.player = getPlayer()
        self.template = self.__tpl.format(self.settings[GLOBAL.COLOR], self.settings['text_size'])
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded += self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved += self.onVehicleMarkerRemoved
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleMarkerRemoved

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        self.as_setUpdateEnabled(False)
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded -= self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved -= self.onVehicleMarkerRemoved
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleMarkerRemoved
        super(Distance, self)._dispose()

    def onVehicleMarkerAdded(self, vProxy, vInfo, guiProps):
        if self.isPostmortem:
            return
        if guiProps == PLAYER_GUI_PROPS.enemy and vProxy.isAlive():
            self.vehicles[vInfo.vehicleID] = vProxy
        self.as_setUpdateEnabled(bool(self.vehicles))

    def onVehicleMarkerRemoved(self, vehicleID, *args, **kwargs):
        if self.isPostmortem:
            return
        if vehicleID in self.vehicles:
            self.vehicles.pop(vehicleID)
        self.as_setUpdateEnabled(bool(self.vehicles))

    @property
    def distances(self):
        for vehicle in self.vehicles.itervalues():
            yield getDistanceToTarget(vehicle, avatar=self.player), vehicle.typeDescriptor.type.shortUserString

    def getUpdatedDistance(self):
        return self.template % min(self.distances) if self.vehicles else super(Distance, self).getUpdatedDistance()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.isPostmortem = ctrlMode in POSTMORTEM_MODES
        if self.isPostmortem:
            self.as_setUpdateEnabled(False)
            self.vehicles.clear()
