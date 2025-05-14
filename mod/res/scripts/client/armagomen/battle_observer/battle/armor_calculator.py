# coding=utf-8

from armagomen._constants import ARMOR_CALC, POSTMORTEM_MODES
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

SETTING_PARAMS = (ARMOR_CALC.SHOW_COUNTED_ARMOR, ARMOR_CALC.SHOW_PIERCING_POWER, ARMOR_CALC.SHOW_PIERCING_RESERVE, ARMOR_CALC.SHOW_CALIBER)


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.calcMacro = dict()
        self.pattern = None
        self.colors = dict()
        self.last_data = None

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
        self.pattern = " | ".join(["%({})d".format(key) for key in SETTING_PARAMS if self.settings[key]])
        for name, code in self.getColors()[ARMOR_CALC.NAME].iteritems():
            self.colors[name] = int(code[1:], 16)

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
        self.as_updateColor(self.colors[color])

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        if ctrlMode in POSTMORTEM_MODES:
            self.as_clearMessage()

    def onArmorChanged(self, data):
        if self.last_data != data:
            self.last_data = data
            if data is None:
                self.as_clearMessage()
            else:
                armor, piercingPower, caliber, ricochet, noDamage = data
                if ricochet or noDamage:
                    self.as_armorCalcS(RICOCHET if ricochet else NO_DAMAGE)
                else:
                    self.calcMacro[ARMOR_CALC.SHOW_COUNTED_ARMOR] = armor
                    self.calcMacro[ARMOR_CALC.SHOW_PIERCING_POWER] = piercingPower
                    self.calcMacro[ARMOR_CALC.SHOW_PIERCING_RESERVE] = piercingPower - armor
                    self.calcMacro[ARMOR_CALC.SHOW_CALIBER] = caliber
                    self.as_armorCalcS(self.pattern % self.calcMacro)
