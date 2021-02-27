from .base_mod_meta import BaseModMeta


class MainGunMeta(BaseModMeta):

    def __init__(self):
        super(MainGunMeta, self).__init__()

    def as_mainGunTextS(self, text):
        return self.flashObject.as_mainGunText(text) if self._isDAAPIInited() else None
