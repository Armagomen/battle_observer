from account_helpers.settings_core.options import CarouselTypeSetting, DoubleCarouselTypeSetting
from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, CAROUSEL
from armagomen.utils.common import overrideMethod
from gui.shared.personality import ServicesLocator


@overrideMethod(CarouselTypeSetting, "getRowCount")
def getRowCount(base, *args, **kwargs):
    return settings.tank_carousel[CAROUSEL.ROWS] if settings.tank_carousel[GLOBAL.ENABLED] else base(*args, **kwargs)


@overrideMethod(CarouselTypeSetting, "getDefaultValue")
def getDefaultValue(base, *args):
    if settings.tank_carousel[CAROUSEL.SMALL] and settings.tank_carousel[GLOBAL.ENABLED]:
        return DoubleCarouselTypeSetting.DOUBLE_CAROUSEL_TYPES.index(DoubleCarouselTypeSetting.OPTIONS.SMALL)
    return base(*args)


@overrideMethod(CarouselTypeSetting, "enableSmallCarousel")
def enableSmallCarousel(base, *args):
    return settings.tank_carousel[CAROUSEL.SMALL] and settings.tank_carousel[GLOBAL.ENABLED] or base(*args)


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


settings.onModSettingsChanged += onModSettingsChanged
