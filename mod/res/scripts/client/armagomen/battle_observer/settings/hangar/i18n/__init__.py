from helpers import getClientLanguage

if getClientLanguage().lower() in ('ru', 'uk', 'be'):
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization
