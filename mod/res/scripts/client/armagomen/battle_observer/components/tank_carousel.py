from armagomen._constants import CAROUSEL, GLOBAL
from armagomen.battle_observer.settings import user
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.lobby.hangar.carousels import TankCarousel
from gui.Scaleform.genConsts.HANGAR_ALIASES import HANGAR_ALIASES
from gui.shared.personality import ServicesLocator


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


user.onModSettingsChanged += onModSettingsChanged


@overrideMethod(TankCarousel, "as_rowCountS")
def as_rowCountS(base, carousel, row_count):
    if user.tank_carousel[GLOBAL.ENABLED] and carousel.getAlias() == HANGAR_ALIASES.TANK_CAROUSEL:
        row_count = max(user.tank_carousel[CAROUSEL.ROWS], row_count)
    return base(carousel, row_count)


@overrideMethod(TankCarousel, "as_setSmallDoubleCarouselS")
def as_setSmallDoubleCarouselS(base, carousel, small):
    return base(carousel, small or user.tank_carousel[GLOBAL.ENABLED] and user.tank_carousel[CAROUSEL.SMALL])
