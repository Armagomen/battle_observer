from armagomen.utils.common import addCallback
from CurrentVehicle import g_currentVehicle
from Event import Event, SafeEvent


class BOEvent(Event):

    def __call__(self, *args, **kwargs):
        for delegate in self:
            delegate(*args, **kwargs)


class Events(object):

    def __init__(self):
        self.onArmorChanged = BOEvent()
        self.onMarkerColorChanged = BOEvent()
        self.onVehicleChangedDelayed = SafeEvent()

        self.onModSettingsChanged = SafeEvent()
        self.onUserConfigUpdateComplete = SafeEvent()

    def subscribe(self):
        g_currentVehicle.onChanged += self.onChangedDelayed

    def unsubscribe(self):
        g_currentVehicle.onChanged -= self.onChangedDelayed

    def onChangedDelayed(self):
        addCallback(0.4, self.onVehicleChangedDelayed, g_currentVehicle.item)


g_events = Events()
