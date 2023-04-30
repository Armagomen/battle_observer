from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, CAROUSEL
from armagomen.utils.common import overrideMethod
from gui.Scaleform.daapi.view.lobby.hangar.carousels import TankCarousel
from gui.Scaleform.genConsts.HANGAR_ALIASES import HANGAR_ALIASES
from gui.shared.personality import ServicesLocator


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


settings.onModSettingsChanged += onModSettingsChanged


@overrideMethod(TankCarousel, "as_rowCountS")
def as_rowCountS(base, carousel, row_count):
    if settings.tank_carousel[GLOBAL.ENABLED] and carousel.getAlias() == HANGAR_ALIASES.TANK_CAROUSEL:
        row_count = max(settings.tank_carousel[CAROUSEL.ROWS], row_count)
    return base(carousel, row_count)


@overrideMethod(TankCarousel, "as_setSmallDoubleCarouselS")
def as_setSmallDoubleCarouselS(base, carousel, small):
    return base(carousel, small or settings.tank_carousel[GLOBAL.ENABLED] and settings.tank_carousel[CAROUSEL.SMALL])
