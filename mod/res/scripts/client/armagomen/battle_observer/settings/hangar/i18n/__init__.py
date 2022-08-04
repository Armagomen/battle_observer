from helpers import getClientLanguage

if getClientLanguage().lower() == 'uk':
    from armagomen.battle_observer.settings.hangar.i18n.uk import localization
elif getClientLanguage().lower() in ('ru', 'be'):
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization
