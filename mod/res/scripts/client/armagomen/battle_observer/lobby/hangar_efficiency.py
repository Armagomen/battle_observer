from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.meta.lobby.base_mod_meta import SHOWING_STATUS_TO_VALUE
from armagomen.battle_observer.meta.lobby.hangar_efficiency_meta import HangarEfficiencyMeta
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug

from gui.impl.lobby.hangar.random.random_hangar import RandomHangar
from gui.impl.lobby.mode_selector.mode_selector_view import ModeSelectorView


class HangarEfficiency(HangarEfficiencyMeta):
    EFFICIENCY_ICONS = {
        "assistIcon": "<img src='{}/efficiency/help.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "blockedIcon": "<img src='{}/efficiency/armor.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "damageIcon": "<img src='{}/efficiency/damage.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "winRateIcon": "<img src='{}/efficiency/wins.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "stunIcon": "<img src='{}/efficiency/stun.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "spottedIcon": "<img src='{}/efficiency/detection.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "battlesIcon": "<img src='{}/efficiency/battles.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    }

    def __init__(self):
        super(HangarEfficiency, self).__init__()
        self.is_hangar = False

    def _populate(self):
        super(HangarEfficiency, self)._populate()
        g_events.onModSettingsChanged += self.onModSettingsChanged
        cachedVehicleData.onChanged += self.update

    def _dispose(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        cachedVehicleData.onChanged += self.update
        super(HangarEfficiency, self)._dispose()

    def getString(self, data):
        value = GLOBAL.EMPTY_LINE
        settings_map = [
            (AVG_EFFICIENCY_HANGAR.DAMAGE, "{damageIcon}{tankAvgDamage}"),
            (AVG_EFFICIENCY_HANGAR.ASSIST, "{assistIcon}{tankAvgAssist}"),
            (AVG_EFFICIENCY_HANGAR.BLOCKED, "{blockedIcon}{tankAvgBlocked}"),
            (AVG_EFFICIENCY_HANGAR.STUN, "{stunIcon}{tankAvgStun}", data.tankAvgStun),
            (AVG_EFFICIENCY_HANGAR.BATTLES, "{battlesIcon}{battles}"),
            (AVG_EFFICIENCY_HANGAR.WIN_RATE, "{winRateIcon}{winRate:.2f}%"),
            (AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN, "{marksOnGunIcon}{marksOnGunValue:.2f}%", data.marksAvailable)
        ]
        text = [tpl[1] for tpl in settings_map if self.getSettings().get(tpl[0]) and tpl[-1]]
        if text:
            params = data._asdict()
            params.update(self.EFFICIENCY_ICONS)
            value = "  ".join(text).format(**params)
        logDebug("Hangar Efficiency Data: {}", value)
        return value

    def update(self, data):
        if data is None:
            return self.as_updateValue("NO DATA, PLAY 1 BATTLE")
        self.as_updateValue(self.getString(data))

    def onModSettingsChanged(self, name, data):
        if name == AVG_EFFICIENCY_HANGAR.NAME:
            self.as_onSettingsChanged(data)
            if data[GLOBAL.ENABLED]:
                cachedVehicleData.onVehicleChanged()

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        window = self.gui.windowsManager.getWindow(uniqueID).content
        logDebug("Hangar Efficiency Window: {}", repr(window))

        if isinstance(window, RandomHangar) and newStatus in SHOWING_STATUS_TO_VALUE:
            self.is_hangar = SHOWING_STATUS_TO_VALUE[newStatus]
            self.setVisible(self.is_hangar)
        if isinstance(window, ModeSelectorView) and newStatus in SHOWING_STATUS_TO_VALUE:
            self.setVisible(self.is_hangar and not SHOWING_STATUS_TO_VALUE[newStatus])
