from armagomen.constants import GLOBAL

if GLOBAL.UKR_LOCALIZATION:
    from armagomen.battle_observer.settings.hangar.i18n.uk import localization
elif GLOBAL.RU_LOCALIZATION:
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization
