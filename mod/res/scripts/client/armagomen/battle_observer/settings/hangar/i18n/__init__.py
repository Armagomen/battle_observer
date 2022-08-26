from helpers import getClientLanguage

language = getClientLanguage()
if language == 'uk':
    from armagomen.battle_observer.settings.hangar.i18n.uk import localization
elif language in ('ru', 'be'):
    from armagomen.battle_observer.settings.hangar.i18n.ru import localization
else:
    from armagomen.battle_observer.settings.hangar.i18n.en import localization
