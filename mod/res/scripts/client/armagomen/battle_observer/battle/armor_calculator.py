# coding=utf-8

from armagomen._constants import ARMOR_CALC, ARMOR_CALC_PARAMS, IMAGE_DIR, POSTMORTEM_MODES
from armagomen.battle_observer.i18n.armor_calculator import NO_DAMAGE, RICOCHET
from armagomen.battle_observer.meta.battle.armor_calc_meta import ArmorCalcMeta
from armagomen.utils.common import hexToInt
from armagomen.utils.events import g_events
from gui.battle_control import avatar_getter


class ArmorCalculator(ArmorCalcMeta):
    DEFAULT_COLOR = 4294967295

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self.pattern = str()
        self.colors = dict()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.setPattern()
        self.colors.update((name, hexToInt(code)) for name, code in self.getColors()[ARMOR_CALC.NAME].items())
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        g_events.onArmorChanged += self.onArmorChanged
        g_events.onMarkerColorChanged += self.onMarkerColorChanged

    def setPattern(self):
        element = "{%d:.0f}"
        splitter = self.settings["splitter"]
        if self.settings[ARMOR_CALC.SHOW_ICONS]:
            img = "<img src='{}/armor_calculator/%d.png' width='16' height='16' vspace='-2'> ".format(IMAGE_DIR)
            element = img + element
            self.pattern = splitter.join(element % (i, i) for i, key in enumerate(ARMOR_CALC_PARAMS) if self.settings[key])
        else:
            self.pattern = splitter.join(element % i for i, key in enumerate(ARMOR_CALC_PARAMS) if self.settings[key])

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
        self.as_updateColor(self.colors.get(color, self.DEFAULT_COLOR))

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
                self.as_armorCalcS(self.pattern.format(armor, piercing_power, caliber, piercing_power - armor))
