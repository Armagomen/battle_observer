from helpers import getClientLanguage
from ....bo_constants import GLOBAL

lang = getClientLanguage().lower()


def getLocalization():
    if lang in GLOBAL.RU_LOCALIZATION:
        from .ru import translate
    elif lang == "de":
        from .de import translate
    else:
        from .en import translate
    return translate


localization = getLocalization()
