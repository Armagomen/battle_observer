from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import AVG_EFFICIENCY_HANGAR, GLOBAL
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


ICONS = {
    "assistIcon": "<img src='{dir}/help.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "blockedIcon": "<img src='{dir}/armor.png' {size} vspace='-9'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "damageIcon": "<img src='{dir}/damage.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "stunIcon": "<img src='{dir}/stun.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR)
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
    if settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN] and data.marksAvailable:
        text.append("{marksOnGunIcon}{marksOnGunValue}%")
    if text:
        params = data._asdict()
        params.update(ICONS)
        return "<font face='$TitleFont' size='20' color='#FAFAFA'>{}</font>".format(" ".join(text).format(**params))
    return ""


def onModSettingsChanged(config, blockID):
    if blockID == AVG_EFFICIENCY_HANGAR.NAME:
        g_currentVehicle.onChanged()


settings.onModSettingsChanged += onModSettingsChanged
