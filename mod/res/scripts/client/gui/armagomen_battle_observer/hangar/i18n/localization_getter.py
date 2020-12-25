from helpers import getClientLanguage

lang = getClientLanguage().lower()


def getLocalization():
    if lang in ('ru', 'uk', 'be'):
        from .ru import translate
    elif lang == "de":
        from .de import translate
    else:
        from .en import translate
    return translate


localization = getLocalization()
