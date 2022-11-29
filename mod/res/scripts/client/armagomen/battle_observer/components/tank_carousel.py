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
def as_rowCountS(base, carousel, rowCount):
    if settings.tank_carousel[GLOBAL.ENABLED] and carousel.getAlias() == HANGAR_ALIASES.TANK_CAROUSEL:
        return base(carousel, settings.tank_carousel[CAROUSEL.ROWS])
    return base(carousel, rowCount)


@overrideMethod(TankCarousel, "as_setSmallDoubleCarouselS")
def as_setSmallDoubleCarouselS(base, carousel, small):
    if settings.tank_carousel[GLOBAL.ENABLED] and carousel.getAlias() == HANGAR_ALIASES.TANK_CAROUSEL:
        return base(carousel, settings.tank_carousel[CAROUSEL.SMALL] or small)
    return base(carousel, small)
