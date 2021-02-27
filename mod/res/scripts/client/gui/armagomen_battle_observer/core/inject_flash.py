from gui.Scaleform.battle_entry import BattleEntry
from gui.Scaleform.daapi.settings import config
from gui.Scaleform.lobby_entry import LobbyEntry
from .bo_constants import SWF
from .utils import overrideMethod


class InjectFlash(object):
    def __init__(self):
        config.BATTLE_PACKAGES += ("gui.armagomen_battle_observer.battle",)
        config.LOBBY_PACKAGES += ("gui.armagomen_battle_observer.lobby",)

    @staticmethod
    @overrideMethod(BattleEntry, "_getRequiredLibraries")
    @overrideMethod(LobbyEntry, "_getRequiredLibraries")
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
