from armagomen.battle_observer.core import cachedVehicleData
from armagomen.battle_observer.meta.lobby.avg_data_meta import AvgDataMeta
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import AVG_EFFICIENCY_HANGAR
from armagomen.utils.events import g_events


class AvgData(AvgDataMeta):

    def _populate(self):
        super(AvgData, self)._populate()
        g_events.onAVGDataUpdated += self.updateAvgData
        settings.onModSettingsChanged += self.onModSettingsChanged
        self.as_startUpdateS(settings.avg_efficiency_in_hangar)
        self.updateAvgData(cachedVehicleData.efficiencyAvgData)

    def _dispose(self):
        super(AvgData, self)._dispose()
        g_events.onAVGDataUpdated -= self.updateAvgData
        settings.onModSettingsChanged -= self.onModSettingsChanged

    def onModSettingsChanged(self, config, blockID):
        if blockID == AVG_EFFICIENCY_HANGAR.NAME:
            self.as_startUpdateS(config)
            self.updateAvgData(cachedVehicleData.efficiencyAvgData)

    def updateAvgData(self, data):
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
            params.update(settings.avg_efficiency_in_hangar[AVG_EFFICIENCY_HANGAR.ICONS])
            return self.as_setDataS(" ".join(text).format(**params))
        self.as_setDataS("")
