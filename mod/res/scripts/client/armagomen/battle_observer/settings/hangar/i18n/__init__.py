from armagomen.constants import GLOBAL


def getLocalization():
    if GLOBAL.RU_LOCALIZATION:
        from armagomen.battle_observer.settings.hangar.i18n.ru import translate
    else:
        from armagomen.battle_observer.settings.hangar.i18n.en import translate
    return translate


localization = getLocalization()
