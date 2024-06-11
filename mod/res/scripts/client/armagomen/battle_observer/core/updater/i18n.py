# coding=utf-8
from helpers import getClientLanguage

en = {
    "titleOK": "Update - Press RESTART",
    "messageOK": "Click RESTART to complete the Upgrade process. v{0}\n",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Choose a download option.</b></font>\n"
        "<p align='left'><font color ='#00FF00'><b>Automatically</b></font> - download and unpack the archive"
        "updates to the folder {0}\n<font color='#FFFF00'><b>Manually</b></font> - opens a link to the installer in "
        "the browser, you will need to install manually.</p>"
        "\n<font size='20 'color='#FFFF00'><b>Changelog</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "<font size='20'>Update available <font color='#FFFF00'>v{0}</font></font>"
}

uk = {
    "titleOK": "Оновлення готове",
    "messageOK": "Натисніть ПЕРЕЗАВАНТАЖЕННЯ для завершення процесу оновлення. v{0}\n",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Оберіть варіант завантаження.</b></font>\n"
        "<p align='left'><font color='#00FF00'><b>Автоматично</b></font> - завантажить і розпакує архів "
        "оновлення в папку. {0}\n<font color='#FFFF00'><b>Вручну</b></font> - відкриває в браузері посилання на "
        "інсталятор, встановлювати потрібно буде в ручному режимі.</p>"
        "\n<font size='20' color='#FFFF00'><b>Список змін</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "<font size='20'>Доступне оновлення <font color='#FFFF00'>v{0}</font></font>"
}


def getI18n():
    if getClientLanguage().lower() in ("uk", "be", "ru"):
        return uk
    else:
        return en
