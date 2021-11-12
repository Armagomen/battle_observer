from armagomen.constants import MAIN
from armagomen.utils.common import overrideMethod
from gui.game_control.PromoController import PromoController
from armagomen.battle_observer.core import settings

# Remove field mail in hangar
@overrideMethod(PromoController, "__tryToShowTeaser")
def __tryToShowTeaser(base, *args):
    if not settings.main[MAIN.FIELD_MAIL]:
        return base(*args)
