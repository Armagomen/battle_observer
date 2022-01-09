from armagomen.constants import GLOBAL

if GLOBAL.RU_LOCALIZATION:
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization
