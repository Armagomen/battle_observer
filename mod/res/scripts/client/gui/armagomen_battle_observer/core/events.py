from Event import SafeEvent


class Events(object):

    def __init__(self):
        self.onHealthChanged = SafeEvent()
        self.onVehicleAddUpdate = SafeEvent()
        self.onVehicleAddPanels = SafeEvent()
        self.onMainGunHealthChanged = SafeEvent()
        self.onPlayerVehicleDeath = SafeEvent()
        self.onPlayerKilledEnemy = SafeEvent()
        self.onKeyPressed = SafeEvent()
        self.updateStatus = SafeEvent()
        self.updateHealthPoints = SafeEvent()
        self.onSettingsChanged = SafeEvent()
        self.onUserConfigUpdateComplete = SafeEvent()
        self.onPlayerShooting = SafeEvent()
        self.setInAoI = SafeEvent()
        self.onEnterBattlePage = SafeEvent()
        self.onExitBattlePage = SafeEvent()
        self.onDispersionAngleUpdate = SafeEvent()


g_events = Events()
