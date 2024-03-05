from Event import SafeEvent


class Events(object):

    def __init__(self):
        self.onArmorChanged = SafeEvent()
        self.onMarkerColorChanged = SafeEvent()
        self.onDispersionAngleChanged = SafeEvent()
        self.updateVehicleData = SafeEvent()
        self.onComponentVisible = SafeEvent()
        self.onVehicleChanged = SafeEvent()
        self.onVehicleChangedDelayed = SafeEvent()
        self.onHangarLoaded = SafeEvent()


g_events = Events()
