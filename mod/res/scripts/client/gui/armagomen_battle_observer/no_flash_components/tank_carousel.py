from account_helpers.settings_core.options import CarouselTypeSetting, DoubleCarouselTypeSetting
from gui.shared.personality import ServicesLocator
from ..core import cfg, cache
from ..core.bo_constants import GLOBAL, CAROUSEL
from ..core.utils.common import overrideMethod


@overrideMethod(CarouselTypeSetting, "getRowCount")
def getRowCount(base, *args, **kwargs):
    return cfg.tank_carousel[CAROUSEL.ROWS] if cfg.tank_carousel[GLOBAL.ENABLED] else base(*args, **kwargs)


@overrideMethod(DoubleCarouselTypeSetting, "enableSmallCarousel")
def enableSmallCarousel(base, *args, **kwargs):
    return cfg.tank_carousel[CAROUSEL.SMALL] and cfg.tank_carousel[GLOBAL.ENABLED] or base(*args, **kwargs)


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


cache.onModSettingsChanged += onModSettingsChanged
