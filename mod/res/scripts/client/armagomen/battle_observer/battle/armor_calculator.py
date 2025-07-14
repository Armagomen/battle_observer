# coding=utf-8

from armagomen._constants import ARMOR_CALC, POSTMORTEM_MODES
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.utils.events import g_events
from armagomen.utils.logging import logWarning
from gui.battle_control import avatar_getter
from helpers import getClientLanguage

language = getClientLanguage().lower()

if language == "uk":
    NO_DAMAGE = "Крит без шкоди"
    RICOCHET = "Рикошет"
elif language in ("ru", "be"):
    NO_DAMAGE = "Крит без урона"
    RICOCHET = "Рикошет"
else:
    NO_DAMAGE = "Non-damaging crit"
    RICOCHET = "Ricochet"

SETTING_PARAMS = (ARMOR_CALC.SHOW_COUNTED_ARMOR, ARMOR_CALC.SHOW_PIERCING_POWER, ARMOR_CALC.SHOW_PIERCING_RESERVE, ARMOR_CALC.SHOW_CALIBER)


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.pattern = None
        self.colors = dict()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.pattern = " | ".join("{%d:d}" % i for i, key in enumerate(SETTING_PARAMS) if self.settings[key])
        if not self.pattern:
            return logWarning("calc message is disabled - no params checked")
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_events.onArmorChanged += self.onArmorChanged
        g_events.onMarkerColorChanged += self.onMarkerColorChanged
        for name, code in self.getColors()[ARMOR_CALC.NAME].iteritems():
            self.colors[name] = int(code[1:], 16)

    def _dispose(self):
        if self.pattern:
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
        if data is None:
            self.as_clearMessage()
        else:
            armor, piercing_power, caliber, ricochet, no_damage = data
            if ricochet:
                self.as_armorCalcS(RICOCHET)
            elif no_damage:
                self.as_armorCalcS(NO_DAMAGE)
            elif self.pattern:
                self.as_armorCalcS(self.pattern.format(armor, piercing_power, piercing_power - armor, caliber))
