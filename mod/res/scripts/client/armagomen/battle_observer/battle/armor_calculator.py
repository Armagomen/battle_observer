# coding=utf-8
from collections import defaultdict

from armagomen._constants import ARMOR_CALC, COLORS, GLOBAL, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.utils.events import g_events
from gui.battle_control import avatar_getter
from helpers import getClientLanguage

language = getClientLanguage().lower()

if language == "uk":
    NO_DAMAGE = "Критичне влучання, без шкоди."
    RICOCHET = "Рикошет."
elif language in ("ru", "be"):
    NO_DAMAGE = "Критическое попадание, без урона."
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

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onArmorChanged -= self.onArmorChanged
        g_events.onMarkerColorChanged -= self.onMarkerColorChanged
        super(ArmorCalculator, self)._dispose()

    def onMarkerColorChanged(self, color):
        self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.getColors()[ARMOR_CALC.NAME].get(color, COLORS.C_RED)
        self.calcMacro[ARMOR_CALC.MACROS_MESSAGE] = self.settings[ARMOR_CALC.MESSAGES].get(color, GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM_MODES:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)

    def onArmorChanged(self, data):
        if data is None:
            return self.as_armorCalcS(GLOBAL.EMPTY_LINE)
        armor, piercingPower, caliber, ricochet, noDamage = data
        self.calcMacro[ARMOR_CALC.RICOCHET] = RICOCHET if ricochet else GLOBAL.EMPTY_LINE
        self.calcMacro[ARMOR_CALC.NO_DAMAGE] = NO_DAMAGE if noDamage else GLOBAL.EMPTY_LINE
        self.calcMacro[ARMOR_CALC.MACROS_COUNTED_ARMOR] = armor
        self.calcMacro[ARMOR_CALC.PIERCING_POWER] = piercingPower
        self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = piercingPower - armor
        self.calcMacro[ARMOR_CALC.MACROS_CALIBER] = caliber
        self.as_armorCalcS(self.settings[ARMOR_CALC.TEMPLATE] % self.calcMacro)
