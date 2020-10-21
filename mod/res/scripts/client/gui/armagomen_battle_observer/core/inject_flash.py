from gui.Scaleform.battle_entry import BattleEntry
from gui.Scaleform.daapi.settings import config
from gui.Scaleform.lobby_entry import LobbyEntry
from .bo_constants import SWF


class Flash(object):

    def inject(self):
        get_librariesBattle = BattleEntry._getRequiredLibraries
        get_librariesLobby = LobbyEntry._getRequiredLibraries
        BattleEntry._getRequiredLibraries = lambda b_self: self.add_libs(get_librariesBattle, b_self)
        LobbyEntry._getRequiredLibraries = lambda b_self: self.add_libs(get_librariesLobby, b_self)
        config.BATTLE_PACKAGES += ("gui.armagomen_battle_observer.battle",)
        config.LOBBY_PACKAGES += ("gui.armagomen_battle_observer.lobby",)

    @staticmethod
    def add_libs(baseMethod, entry):
        libs = baseMethod(entry)
        isTuple = isinstance(libs, tuple)
        if isTuple:
            libs = list(libs)
        if isinstance(entry, LobbyEntry) and SWF.LOBBY not in libs:
            libs.append(SWF.LOBBY)
        elif isinstance(entry, BattleEntry) and SWF.BATTLE not in libs:
            libs.append(SWF.BATTLE)
        return libs if not isTuple else tuple(libs)


g_flash = Flash()
