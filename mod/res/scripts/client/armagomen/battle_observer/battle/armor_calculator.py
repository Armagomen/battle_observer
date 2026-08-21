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

    @staticmethod
    def getElement(key, idx, with_icon):
        """
        Returns the prepared template fragment for a single parameter:
        - with an icon (if with_icon=True) or without;
        - using an indexed placeholder "{N:.0f}" or "{N:.0%}".
        """
        # indexed placeholder, e.g. "{2:.0f}" or "{3:.0%}"

        if key != ARMOR_CALC.SHOW_CHANCE:
            placeholder = '{{{0}:.0f}}'.format(idx)
        else:
            placeholder = '{{{0}:.0%}}'.format(idx)

        if with_icon:
            img = "<img src='{0}/armor_calculator/{1}.png' width='20' height='20' vspace='-4'> ".format(IMAGE_DIR, idx)
            return img + placeholder
        return placeholder

    def setPattern(self):
        with_icon = self.settings[ARMOR_CALC.SHOW_ICONS]
        sep = "  " if with_icon else " | "
        self.pattern = sep.join(self.getElement(key, i, with_icon) for i, key in enumerate(ARMOR_CALC_PARAMS) if self.settings[key])

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
            armor, piercing_power, caliber, ricochet, no_damage, chance = data
            if ricochet:
                self.as_armorCalcS(RICOCHET)
            elif no_damage:
                self.as_armorCalcS(NO_DAMAGE)
            elif self.pattern:
                self.as_armorCalcS(self.pattern.format(armor, piercing_power, caliber, piercing_power - armor, chance))
