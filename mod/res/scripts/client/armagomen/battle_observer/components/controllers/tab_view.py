from armagomen._constants import GLOBAL, MAIN, STATISTICS, STATISTICS_REGION
from armagomen.utils.common import addCallback, toggleOverride
from armagomen.utils.events import g_events
from gui.impl.gen.view_models.common.badge_model import BadgeModel
from gui.impl.gen.view_models.common.battle_player import BattlePlayer


def cleanString(base, model, value):
    return base(model, "")


__players = {}


def setVehicleId(base, player, value):
    base(player, value)
    __players[value] = player


def cleanup():
    __players.clear()


def getTabItems():
    return __players


def addWGR(vehicleId, wgr, is_enemy):
    if __players and vehicleId in __players:
        player = __players[vehicleId]
        name = player.getUserName()
        pattern = [name[:min(len(name), 9)], str(wgr)]
        player.setUserName(" | ".join(pattern if is_enemy else reversed(pattern)))
    else:
        addCallback(1.0, addWGR, vehicleId, wgr, is_enemy)


def _onModSettingsChanged(name, data):
    if name == MAIN.NAME:
        toggleOverride(BattlePlayer, "setClanAbbrev", cleanString, data[MAIN.HIDE_CLAN_ABBREV])
        toggleOverride(BadgeModel, "setLevel", cleanString, data[MAIN.HIDE_BADGES])
        toggleOverride(BadgeModel, "setBadgeID", cleanString, data[MAIN.HIDE_BADGES])
    elif name == STATISTICS.NAME:
        toggleOverride(BattlePlayer, "setVehicleId", setVehicleId,
                       data[GLOBAL.ENABLED] and data[STATISTICS.STATISTIC_ENABLED] and STATISTICS_REGION)


g_events.onModSettingsChanged += _onModSettingsChanged


def fini():
    g_events.onModSettingsChanged -= _onModSettingsChanged
