from collections import defaultdict

from armagomen.constants import ARMOR_CALC, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.utils.common import events
from gui.battle_control import avatar_getter


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.messages = None
        self._cache = GLOBAL.ZERO
        self.calcMacro = None
        self.typeColors = None
        self.template = None

    def onEnterBattlePage(self):
        super(ArmorCalculator, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        events.onArmorChanged += self.onArmorChanged
        events.onMarkerColorChanged += self.onMarkerColorChanged

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        events.onArmorChanged -= self.onArmorChanged
        events.onMarkerColorChanged -= self.onMarkerColorChanged
        super(ArmorCalculator, self).onExitBattlePage()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.messages = self.settings[ARMOR_CALC.MESSAGES]
        self.calcMacro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.typeColors = self.colors[ARMOR_CALC.NAME]
        self.template = self.settings[ARMOR_CALC.TEMPLATE]
        self.as_startUpdateS(self.settings)

    def onMarkerColorChanged(self, color):
        self.calcMacro[ARMOR_CALC.MACROS_MESSAGE] = self.messages.get(color, GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)
        if ctrlMode in POSTMORTEM.MODES:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)

    def onArmorChanged(self, countedArmor, penetration, caliber, color, ricochet):
        if self._cache != countedArmor:
            self._cache = countedArmor
            if countedArmor is not None:
                self.calcMacro[ARMOR_CALC.MACROS_RICOCHET] = "ricochet" if ricochet else GLOBAL.EMPTY_LINE
                self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.typeColors[color]
                self.calcMacro[ARMOR_CALC.MACROS_COUNTED_ARMOR] = countedArmor
                self.calcMacro[ARMOR_CALC.PIERCING_POWER] = penetration
                self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = penetration - countedArmor
                self.calcMacro[ARMOR_CALC.MACROS_CALIBER] = caliber
                self.as_armorCalcS(self.template % self.calcMacro)
            else:
                self.as_armorCalcS(GLOBAL.EMPTY_LINE)
