from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class FlightTimeMeta(BaseModMeta):

    def __init__(self):
        super(FlightTimeMeta, self).__init__()

    def as_flightTimeS(self, text):
        if self._isDAAPIInited():
            self.flashObject.as_flightTime(text)
