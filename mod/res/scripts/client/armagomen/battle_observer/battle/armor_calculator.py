from collections import defaultdict

from armagomen.battle_observer.core import config, b_core
from armagomen.battle_observer.core.bo_constants import ARMOR_CALC, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from gui.battle_control import avatar_getter
from gui.shared.personality import ServicesLocator

settingsCore = ServicesLocator.settingsCore


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self._visible = False
        self.messages = config.armor_calculator[ARMOR_CALC.MESSAGES]
        self.calcCache = GLOBAL.ZERO
        self.calcMacro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.typeColors = config.colors[ARMOR_CALC.NAME]
        self.template = config.armor_calculator[ARMOR_CALC.TEMPLATE]
        self.showCalcPoints = config.armor_calculator[ARMOR_CALC.SHOW_POINTS]
        self.currentShellID = None

    def onEnterBattlePage(self):
        super(ArmorCalculator, self).onEnterBattlePage()
        ammo = self.sessionProvider.shared.ammo
        if ammo is not None:
            ammo.onGunReloadTimeSet += self.onGunReload
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        b_core.onArmorChanged += self.onArmorChanged
        b_core.onMarkerColorChanged += self.onMarkerColorChanged
        self.updateShootParams()

    def onExitBattlePage(self):
        ammo = self.sessionProvider.shared.ammo
        if ammo is not None:
            ammo.onGunReloadTimeSet -= self.onGunReload
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        b_core.onArmorChanged -= self.onArmorChanged
        b_core.onMarkerColorChanged += self.onMarkerColorChanged
        super(ArmorCalculator, self).onExitBattlePage()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.as_startUpdateS(config.armor_calculator)

    def onMarkerColorChanged(self, color):
        if color == ARMOR_CALC.NORMAL:
            self.clearView()
        else:
            self.calcMacro[ARMOR_CALC.MACROS_MESSAGE] = self.messages.get(color, GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.clearView()

    def updateShootParams(self):
        shot_params = self._player.getVehicleDescriptor().shot
        p100 = shot_params.piercingPower[GLOBAL.FIRST]
        self.calcMacro.update(piercingPower=p100, caliber=shot_params.shell.caliber)

    def onGunReload(self, shellID, state):
        if shellID != self.currentShellID:
            self.currentShellID = shellID
            self.updateShootParams()
            if self._visible:
                self.as_armorCalcS(self.template % self.calcMacro)

    def onArmorChanged(self, armorSum, color, countedArmor):
        if self.calcCache != countedArmor:
            self._visible = armorSum is not None
            self.calcCache = countedArmor
            if countedArmor:
                self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.typeColors[color]
                self.calcMacro[ARMOR_CALC.MACROS_CALCED_ARMOR] = countedArmor
                self.calcMacro[ARMOR_CALC.MACROS_ARMOR] = armorSum
                self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = \
                    self.calcMacro[ARMOR_CALC.PIERCING_POWER] - countedArmor
                self.as_armorCalcS(self.template % self.calcMacro)

    def clearView(self):
        if self.showCalcPoints:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)
