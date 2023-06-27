from CurrentVehicle import g_currentVehicle
from armagomen._constants import AVG_EFFICIENCY_HANGAR, GLOBAL, IMAGE_DIR, EFFICIENCY_ICONS_SIZE
from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.lobby.hangar.ammunition_panel import AmmunitionPanel


@overrideMethod(AmmunitionPanel, "as_updateVehicleStatusS")
def updateStatus(base, panel, data):
    cachedVehicleData.onVehicleChanged()
    if settings.avg_efficiency_in_hangar[GLOBAL.ENABLED]:
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
}


def getAvgData():
    data = cachedVehicleData.efficiencyAvgData
    text = []
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.DAMAGE]:
        text.append("{damageIcon}{damage}")
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.ASSIST]:
        text.append("{assistIcon}{assist}")
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.BLOCKED]:
        text.append("{blockedIcon}{blocked}")
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.STUN] and data.stun:
        text.append("{stunIcon}{stun}")
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.WIN_RATE]:
        text.append("{winRateIcon}{winRate}%")
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN] and data.marksAvailable:
        text.append("{marksOnGunIcon}{marksOnGunValue}%")
    if text:
        params = data._asdict()
        params.update(EFFICIENCY_ICONS)
        return "<font face='$TitleFont' size='20' color='#FAFAFA'>{}</font>".format("  ".join(text).format(**params))
    return ""


def onModSettingsChanged(config, blockID):
    if blockID == AVG_EFFICIENCY_HANGAR.NAME:
        g_currentVehicle.onChanged()


settings.onModSettingsChanged += onModSettingsChanged
