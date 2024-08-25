from Event import Event, SafeEvent


class BOEvent(Event):

    def __call__(self, *args, **kwargs):
        for delegate in self[:]:
            delegate(*args, **kwargs)


class Events(object):

    def __init__(self):
        self.onArmorChanged = BOEvent()
        self.onMarkerColorChanged = BOEvent()
        self.onDispersionAngleChanged = BOEvent()
        self.onVehicleChanged = SafeEvent()
        self.onVehicleChangedDelayed = SafeEvent()


g_events = Events()
