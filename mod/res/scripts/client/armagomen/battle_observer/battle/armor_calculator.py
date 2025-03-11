# coding=utf-8
from collections import defaultdict

from armagomen._constants import ARMOR_CALC, COLORS, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.components.shot_result_plugin import _updateRandomization
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.utils.events import g_events
from gui.battle_control import avatar_getter
from helpers import getClientLanguage

if getClientLanguage().lower() in ("uk", "be"):
    NO_DAMAGE = "Критичне влучання, без шкоди."
    RICOCHET = "Рикошет."
else:
    NO_DAMAGE = "Critical hit, no damage."
    RICOCHET = "Ricochet."


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.calcMacro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_events.onArmorChanged += self.onArmorChanged
        g_events.onMarkerColorChanged += self.onMarkerColorChanged
        prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
        if prebattleCtrl is not None:
            prebattleCtrl.onVehicleChanged += self.__updateCurrVehicleInfo
            prebattleCtrl.onBattleStarted += self.__updateCurrVehicleInfo

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onArmorChanged -= self.onArmorChanged
        g_events.onMarkerColorChanged -= self.onMarkerColorChanged
        prebattleCtrl = self.sessionProvider.dynamic.prebattleSetup
        if prebattleCtrl is not None:
            prebattleCtrl.onVehicleChanged -= self.__updateCurrVehicleInfo
            prebattleCtrl.onBattleStarted -= self.__updateCurrVehicleInfo
        super(ArmorCalculator, self)._dispose()

    def onMarkerColorChanged(self, color):
        self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.getColors()[ARMOR_CALC.NAME].get(color, COLORS.C_RED)
        self.calcMacro[ARMOR_CALC.MACROS_MESSAGE] = self.settings[ARMOR_CALC.MESSAGES].get(color, GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM_MODES:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)

    def onArmorChanged(self, armor, piercingPower, caliber, ricochet, noDamage):
        if armor is None:
            return self.as_armorCalcS(GLOBAL.EMPTY_LINE)
        self.calcMacro[ARMOR_CALC.RICOCHET] = RICOCHET if ricochet else GLOBAL.EMPTY_LINE
        self.calcMacro[ARMOR_CALC.NO_DAMAGE] = NO_DAMAGE if noDamage else GLOBAL.EMPTY_LINE
        self.calcMacro[ARMOR_CALC.MACROS_COUNTED_ARMOR] = armor
        self.calcMacro[ARMOR_CALC.PIERCING_POWER] = piercingPower
        self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = piercingPower - armor
        self.calcMacro[ARMOR_CALC.MACROS_CALIBER] = caliber
        self.as_armorCalcS(self.settings[ARMOR_CALC.TEMPLATE] % self.calcMacro)

    def __updateCurrVehicleInfo(self, vehicle=None):
        ctrl = self.sessionProvider.dynamic.prebattleSetup
        if ctrl is None:
            return
        else:
            if vehicle is None:
                vehicle = ctrl.getCurrentGUIVehicle()
            if vehicle is not None and not avatar_getter.isObserver():
                _updateRandomization(vehicle)
