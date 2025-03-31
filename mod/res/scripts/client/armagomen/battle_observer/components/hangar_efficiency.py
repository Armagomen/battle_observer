from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from CurrentVehicle import g_currentVehicle
from gui.Scaleform.daapi.view.lobby.hangar.ammunition_panel import AmmunitionPanel

_settings = user_settings.avg_efficiency_in_hangar


def checkCategory():
    return any(value for key, value in _settings.iteritems() if key != GLOBAL.ENABLED)


@overrideMethod(AmmunitionPanel, "as_updateVehicleStatusS")
def updateStatus(base, panel, data):
    cachedVehicleData.onVehicleChanged()
    if _settings[GLOBAL.ENABLED] and checkCategory():
        if data["message"]:
            data["message"] += "\n" + getAvgData()
        else:
            data["message"] = getAvgData()
    return base(panel, data)


EFFICIENCY_ICONS = {
    "assistIcon": "<img src='{}/efficiency/help.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "blockedIcon": "<img src='{}/efficiency/armor.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "damageIcon": "<img src='{}/efficiency/damage.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "winRateIcon": "<img src='{}/efficiency/wins.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "stunIcon": "<img src='{}/efficiency/stun.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "spottedIcon": "<img src='{}/efficiency/detection.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    "battlesIcon": "<img src='{}/efficiency/battles.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
}


def getAvgData():
    data = cachedVehicleData.efficiencyAvgData
    text = []
    if _settings[AVG_EFFICIENCY_HANGAR.DAMAGE]:
        text.append("{damageIcon}{tankAvgDamage}")
    if _settings[AVG_EFFICIENCY_HANGAR.ASSIST]:
        text.append("{assistIcon}{tankAvgAssist}")
    if _settings[AVG_EFFICIENCY_HANGAR.BLOCKED]:
        text.append("{blockedIcon}{tankAvgBlocked}")
    if _settings[AVG_EFFICIENCY_HANGAR.STUN] and data.tankAvgStun:
        text.append("{stunIcon}{tankAvgStun}")
    if _settings[AVG_EFFICIENCY_HANGAR.BATTLES]:
        text.append("{battlesIcon}{battles}")
    if _settings[AVG_EFFICIENCY_HANGAR.WIN_RATE]:
        text.append("{winRateIcon}{winRate}%")
    if _settings[AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN] and data.marksAvailable:
        text.append("{marksOnGunIcon}{marksOnGunValue}%")
    if text:
        params = data._asdict()
        params.update(EFFICIENCY_ICONS)
        return "<font face='$TitleFont' size='20' color='#FAFAFA'>{}</font>".format("  ".join(text).format(**params))
    return GLOBAL.EMPTY_LINE


def _onModSettingsChanged(config, blockID):
    if blockID == AVG_EFFICIENCY_HANGAR.NAME:
        if g_currentVehicle.intCD:
            g_currentVehicle.onChanged()


user_settings.onModSettingsChanged += _onModSettingsChanged


def fini():
    user_settings.onModSettingsChanged -= _onModSettingsChanged
