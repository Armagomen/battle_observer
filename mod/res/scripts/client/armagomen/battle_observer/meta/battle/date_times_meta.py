from armagomen.battle_observer.meta.battle.base_mod_meta import BaseModMeta


class DateTimesMeta(BaseModMeta):

    def __init__(self):
        super(DateTimesMeta, self).__init__()

    def as_setDateTimeS(self, text):
        if self._isDAAPIInited():
            self.flashObject.as_setDateTime(text)
