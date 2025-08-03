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


g_events = Events()
