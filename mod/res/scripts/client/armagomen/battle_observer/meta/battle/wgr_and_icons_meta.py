from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta

class WGRAndIconsMeta(BaseModMeta):

    def as_updateAll(self, milliseconds):
        if self._isDAAPIInited():
            self.flashObject.as_updateAll(milliseconds)

    def as_updateFullStats(self, milliseconds):
        if self._isDAAPIInited():
            self.flashObject.as_updateFullStatsOnkey(milliseconds)

    def as_update_wgr_data(self, itemsData):
        if self._isDAAPIInited():
            self.flashObject.as_update_wgr_data(itemsData)