from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta

class WGRAndIconsMeta(BaseModMeta):

    def as_update_wgr_dataS(self, itemsData):
        if self._isDAAPIInited():
            self.flashObject.as_update_wgr_data(itemsData)