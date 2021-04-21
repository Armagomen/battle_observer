from account_helpers.settings_core.options import CarouselTypeSetting, DoubleCarouselTypeSetting
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.core.bo_constants import GLOBAL, CAROUSEL
from armagomen.utils.common import overrideMethod
from gui.shared.personality import ServicesLocator


@overrideMethod(CarouselTypeSetting, "getRowCount")
def getRowCount(base, *args, **kwargs):
    return settings.tank_carousel[CAROUSEL.ROWS] if settings.tank_carousel[GLOBAL.ENABLED] else base(*args, **kwargs)


@overrideMethod(DoubleCarouselTypeSetting, "enableSmallCarousel")
def enableSmallCarousel(base, *args, **kwargs):
    return settings.tank_carousel[CAROUSEL.SMALL] and settings.tank_carousel[GLOBAL.ENABLED] or base(*args, **kwargs)


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


settings.onModSettingsChanged += onModSettingsChanged
