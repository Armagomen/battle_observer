from account_helpers.settings_core.options import CarouselTypeSetting, DoubleCarouselTypeSetting
from armagomen.battle_observer.core import settings
from armagomen.constants import GLOBAL, CAROUSEL
from armagomen.utils.common import overrideMethod
from gui.shared.personality import ServicesLocator


@overrideMethod(CarouselTypeSetting, "getRowCount")
def getRowCount(base, *args, **kwargs):
    return settings.tank_carousel[CAROUSEL.ROWS] if settings.tank_carousel[GLOBAL.ENABLED] else base(*args, **kwargs)


def onModSettingsChanged(config, blockID):
    if blockID == CAROUSEL.NAME:
        DoubleCarouselTypeSetting.DOUBLE_CAROUSEL_TYPES = (
            DoubleCarouselTypeSetting.OPTIONS.SMALL if config[CAROUSEL.SMALL] and config[
                GLOBAL.ENABLED] else DoubleCarouselTypeSetting.OPTIONS.ADAPTIVE
            , DoubleCarouselTypeSetting.OPTIONS.SMALL
        )
        ServicesLocator.settingsCore.onSettingsChanged(CAROUSEL.SETTINGS)


settings.onModSettingsChanged += onModSettingsChanged
