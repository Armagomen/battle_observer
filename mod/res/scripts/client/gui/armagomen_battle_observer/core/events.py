from Event import SafeEvent


class Events(object):

    def __init__(self):
        self.onVehicleAddUpdate = SafeEvent()
        self.onPlayerVehicleDeath = SafeEvent()
        self.onPlayerKilledEnemy = SafeEvent()
        self.onKeyPressed = SafeEvent()
        self.onSettingsChanged = SafeEvent()
        self.onUserConfigUpdateComplete = SafeEvent()
        self.onPlayerShooting = SafeEvent()
        self.onEnterBattlePage = SafeEvent()
        self.onExitBattlePage = SafeEvent()
        self.onDispersionAngleUpdate = SafeEvent()


g_events = Events()
