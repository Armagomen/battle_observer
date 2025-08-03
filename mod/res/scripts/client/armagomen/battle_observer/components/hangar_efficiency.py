from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.utils.common import toggleOverride
from armagomen.utils.events import g_events
from CurrentVehicle import g_currentVehicle
from gui.Scaleform.daapi.view.lobby.hangar.ammunition_panel import AmmunitionPanel


class HangarEfficiency(object):
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
        self.enabled = False
        self.config = {}
        g_events.onModSettingsChanged += self._onModSettingsChanged

    def updateStatus(self, base, panel, data):
        cachedVehicleData.onVehicleChanged()
        text = self.getAvgData()
        if text:
            data["message"] += ("\n" + text) if data["message"] else text
        return base(panel, data)

    def getAvgData(self):
        data = cachedVehicleData.efficiencyAvgData
        settings_map = [
            (AVG_EFFICIENCY_HANGAR.DAMAGE, "{damageIcon}{tankAvgDamage}"),
            (AVG_EFFICIENCY_HANGAR.ASSIST, "{assistIcon}{tankAvgAssist}"),
            (AVG_EFFICIENCY_HANGAR.BLOCKED, "{blockedIcon}{tankAvgBlocked}"),
            (AVG_EFFICIENCY_HANGAR.STUN, "{stunIcon}{tankAvgStun}", data.tankAvgStun),
            (AVG_EFFICIENCY_HANGAR.BATTLES, "{battlesIcon}{battles}"),
            (AVG_EFFICIENCY_HANGAR.WIN_RATE, "{winRateIcon}{winRate:.2f}%"),
            (AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN, "{marksOnGunIcon}{marksOnGunValue:.2f}%", data.marksAvailable)
        ]
        text = [tpl[1] for tpl in settings_map if self.config.get(tpl[0]) and tpl[-1]]
        if text:
            params = data._asdict()
            params.update(self.EFFICIENCY_ICONS)
            return "<font face='$TitleFont' size='20' color='#FAFAFA'>{}</font>".format("  ".join(text).format(**params))
        return GLOBAL.EMPTY_LINE

    def _onModSettingsChanged(self, config, blockID):
        if blockID == AVG_EFFICIENCY_HANGAR.NAME:
            enabled = config[GLOBAL.ENABLED]
            self.config.update(config)
            if self.enabled != config[GLOBAL.ENABLED]:
                self.enabled = config[GLOBAL.ENABLED]
                toggleOverride(AmmunitionPanel, "as_updateVehicleStatusS", self.updateStatus, self.enabled)
                if g_currentVehicle.intCD:
                    g_currentVehicle.onChanged()


eff = HangarEfficiency()


def fini():
    g_events.onModSettingsChanged -= eff._onModSettingsChanged
