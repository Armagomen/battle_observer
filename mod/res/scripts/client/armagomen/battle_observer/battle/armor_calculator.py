from collections import defaultdict, namedtuple

from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.constants import ARMOR_CALC, GLOBAL, POSTMORTEM, COLORS
from armagomen.utils.events import g_events
from gui.battle_control import avatar_getter

OtherMessages = namedtuple("OtherMessages", ("ricochet", "noDamage"))


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.messages = None
        self._cache = GLOBAL.ZERO
        self.calcMacro = None
        self.typeColors = None
        self.template = None
        self.otherMessages = None

    def onEnterBattlePage(self):
        super(ArmorCalculator, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        g_events.onArmorChanged += self.onArmorChanged
        g_events.onMarkerColorChanged += self.onMarkerColorChanged

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged -= self.onCameraChanged
        g_events.onArmorChanged -= self.onArmorChanged
        g_events.onMarkerColorChanged -= self.onMarkerColorChanged
        super(ArmorCalculator, self).onExitBattlePage()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.messages = self.settings[ARMOR_CALC.MESSAGES]
        self.otherMessages = OtherMessages(
            (GLOBAL.EMPTY_LINE, self.settings[ARMOR_CALC.RICOCHET]),
            (GLOBAL.EMPTY_LINE, self.settings[ARMOR_CALC.NO_DAMAGE])
        )
        self.calcMacro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.typeColors = self.colors[ARMOR_CALC.NAME]
        self.template = self.settings[ARMOR_CALC.TEMPLATE]
        g_events.onCrosshairPositionChanged += self.as_onCrosshairPositionChanged
        self.as_startUpdateS(self.settings)

    def _dispose(self):
        g_events.onCrosshairPositionChanged -= self.as_onCrosshairPositionChanged
        super(ArmorCalculator, self)._dispose()

    def onMarkerColorChanged(self, color):
        self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.typeColors.get(color, COLORS.C_RED)
        self.calcMacro[ARMOR_CALC.MACROS_MESSAGE] = self.messages.get(color, GLOBAL.EMPTY_LINE)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM.MODES:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)

    def onArmorChanged(self, armor, piercingPower, caliber, ricochet, noDamage):
        if self._cache == armor:
            return
        self._cache = armor
        if armor is not None:
            self.calcMacro[ARMOR_CALC.RICOCHET] = self.otherMessages.ricochet[ricochet]
            self.calcMacro[ARMOR_CALC.NO_DAMAGE] = self.otherMessages.noDamage[noDamage]
            self.calcMacro[ARMOR_CALC.MACROS_COUNTED_ARMOR] = armor
            self.calcMacro[ARMOR_CALC.PIERCING_POWER] = piercingPower
            self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = piercingPower - armor
            self.calcMacro[ARMOR_CALC.MACROS_CALIBER] = caliber
            self.as_armorCalcS(self.template % self.calcMacro)
        else:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)
