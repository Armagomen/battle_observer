from Event import SafeEvent


class Events(object):

    def __init__(self):
        self.onArmorChanged = SafeEvent()
        self.onMarkerColorChanged = SafeEvent()
        self.onDispersionAngleChanged = SafeEvent()
        self.onLoginLoaded = SafeEvent()
        self.onHangarLoaded = SafeEvent()
        self.onBattlePageLoaded = SafeEvent()
        self.updateVehicleData = SafeEvent()
        self.onComponentVisible = SafeEvent()
        self.onVehicleChanged = SafeEvent()
        self.onVehicleChangedDelayed = SafeEvent()
        self.onAVGDataUpdated = SafeEvent()


g_events = Events()
