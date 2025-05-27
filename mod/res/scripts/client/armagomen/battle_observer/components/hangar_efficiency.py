from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from CurrentVehicle import g_currentVehicle
from gui.Scaleform.daapi.view.lobby.hangar.ammunition_panel import AmmunitionPanel

_settings = user_settings.avg_efficiency_in_hangar


@overrideMethod(AmmunitionPanel, "as_updateVehicleStatusS")
def updateStatus(base, panel, data):
    cachedVehicleData.onVehicleChanged()
    if _settings[GLOBAL.ENABLED]:
        text = getAvgData()
        if text:
            data["message"] += ("\n" + text) if data["message"] else text
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
    settings_map = [
        (AVG_EFFICIENCY_HANGAR.DAMAGE, "{damageIcon}{tankAvgDamage}"),
        (AVG_EFFICIENCY_HANGAR.ASSIST, "{assistIcon}{tankAvgAssist}"),
        (AVG_EFFICIENCY_HANGAR.BLOCKED, "{blockedIcon}{tankAvgBlocked}"),
        (AVG_EFFICIENCY_HANGAR.STUN, "{stunIcon}{tankAvgStun}", data.tankAvgStun),
        (AVG_EFFICIENCY_HANGAR.BATTLES, "{battlesIcon}{battles}"),
        (AVG_EFFICIENCY_HANGAR.WIN_RATE, "{winRateIcon}{winRate}%"),
        (AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN, "{marksOnGunIcon}{marksOnGunValue}%", data.marksAvailable)
    ]
    text = [tpl[1] for tpl in settings_map if _settings.get(tpl[0]) and (len(tpl) == 2 or tpl[2])]
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
