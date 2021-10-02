from Event import SafeEvent


class Events(object):

    def __init__(self):
        self.onArmorChanged = SafeEvent()
        self.onMarkerColorChanged = SafeEvent()
        self.onDispersionAngleChanged = SafeEvent()
        self.onDisconnected = SafeEvent()
        self.onConnected = SafeEvent()
        self.onHangarLoaded = SafeEvent()
        self.init = SafeEvent()
        self.fini = SafeEvent()


g_events = Events()
