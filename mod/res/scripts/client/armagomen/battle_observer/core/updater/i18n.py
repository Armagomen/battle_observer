# coding=utf-8
from helpers import getClientLanguage

en = {
    "titleOK": "Update - Press RESTART",
    "messageOK": "Click 'Close game' to complete the Upgrade process. v{0}\n",
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
    "messageOK": "Натисніть 'Закрити гру' для завершення процесу оновлення. v{0}\n",
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

ru = {
    "titleOK": "Обновление готово",
    "messageOK": "Нажмите 'Закрыть игру' для завершения процесса обновления. v{0}\n",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Выберите вариант загрузки.</b></font>\n"
        "<p align='left'><font color='#00FF00'><b>Автоматически</b></font> — загрузит и распакует архив "
        "обновления в папку. {0}\n<font color='#FFFF00'><b>Вручную</b></font> — откроет в браузере ссылку на "
        "инсталлятор, устанавливать нужно будет вручную.</p>"
        "\n<font size='20' color='#FFFF00'><b>Список изменений</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "<font size='20'>Доступно обновление <font color='#FFFF00'>v{0}</font></font>"
}


def getI18n():
    ln_code = getClientLanguage().lower()
    if ln_code in ("ru", "be"):
        return ru
    elif ln_code == "uk":
        return uk
    else:
        return en
