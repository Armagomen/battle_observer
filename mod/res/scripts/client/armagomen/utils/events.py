from armagomen.utils.common import addCallback
from CurrentVehicle import g_currentVehicle
from Event import Event, SafeEvent
from helpers import dependency
from skeletons.gui.app_loader import GuiGlobalSpaceID, IAppLoader


class BOEvent(Event):

    def __call__(self, *args, **kwargs):
        for delegate in self:
            delegate(*args, **kwargs)


class Events(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.onArmorChanged = BOEvent()
        self.onMarkerColorChanged = BOEvent()
        self.onVehicleChangedDelayed = SafeEvent()
        self.onModSettingsChanged = SafeEvent()

        self.appLoader.onGUISpaceEntered += self.subscribe
        self.appLoader.onGUISpaceLeft += self.unsubscribe

    def subscribe(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        g_currentVehicle.onChanged += self.onChangedDelayed

    def unsubscribe(self, spaceID):
        if spaceID != GuiGlobalSpaceID.LOBBY:
            return
        g_currentVehicle.onChanged -= self.onChangedDelayed

    def onChangedDelayed(self):
        addCallback(0.2, self.onVehicleChangedDelayed, g_currentVehicle.item)


g_events = Events()
