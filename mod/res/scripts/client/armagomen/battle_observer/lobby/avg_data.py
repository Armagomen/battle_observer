from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.meta.lobby.avg_data_meta import AvgDataMeta
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import AVG_EFFICIENCY_HANGAR, GLOBAL
from armagomen.utils.events import g_events

ICONS = {
    "assistIcon": "<img src='{dir}/help.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "blockedIcon": "<img src='{dir}/armor.png' {size} vspace='-9'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "damageIcon": "<img src='{dir}/damage.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR),
    "stunIcon": "<img src='{dir}/stun.png' {size} vspace='-10'>".format(**GLOBAL.IMG_PARAMS_HANGAR)
}


class AvgData(AvgDataMeta):

    def _populate(self):
        super(AvgData, self)._populate()
        g_events.onAVGDataUpdated += self.updateAvgData
        settings.onModSettingsChanged += self.onModSettingsChanged
        if settings.avg_efficiency_in_hangar[GLOBAL.ENABLED]:
            self.updateAvgData(cachedVehicleData.efficiencyAvgData)

    def _dispose(self):
        super(AvgData, self)._dispose()
        g_events.onAVGDataUpdated -= self.updateAvgData
        settings.onModSettingsChanged -= self.onModSettingsChanged

    def onModSettingsChanged(self, config, blockID):
        if blockID == AVG_EFFICIENCY_HANGAR.NAME:
            self.updateAvgData(cachedVehicleData.efficiencyAvgData)

    def updateAvgData(self, data):
        if settings.avg_efficiency_in_hangar[GLOBAL.ENABLED]:
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
                text.append(" {marksOnGunIcon}{marksOnGunValue}%")
            if text:
                params = data._asdict()
                params.update(ICONS)
                return self.as_setDataS(" ".join(text).format(**params))
        self.as_setDataS(GLOBAL.EMPTY_LINE)
