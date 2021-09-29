from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import PANELS

WTR_COLORS = {2971: "bad", 4530: "normal", 6370: "good", 8525: "very_good", 10158: "unique"}


def getStatisticString(wtr):
    result = "very_bad"
    for value in sorted(WTR_COLORS.iterkeys()):
        if wtr >= value:
            result = WTR_COLORS[value]
        else:
            break
    return settings.players_panels[PANELS.STATISTIC_PATTERN].get(result)
