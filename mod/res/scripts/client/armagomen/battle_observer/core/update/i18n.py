# coding=utf-8
from helpers import getClientLanguage

ru = {
    "titleOK": "\nОбновление - ГОТОВО",
    "messageWAIT": "Подождите, идет загрузка Обновления v{0}",
    "messageOK": "Нажмите ПЕРЕЗАГРУЗКА, для завершения процесса Обновления. v{0}",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Выберите вариант загрузки.</b></font>\n"
        "<p align='left'><font color='#00FF00'><b>Автоматически</b></font> - загрузит и распакует архив "
        "обновления в папку. {0}\n<font color='#FFFF00'><b>Вручную</b></font> - откроет в браузере ссылку на"
        " этот-же архив но извлекать пакет и копировать *.wotmod файл/ы прийдется в ручном режиме.</p>"
        "\n<font size='20' color='#FFFF00'><b>Список изменений</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "\n<font size='20'>Доступно обновление <font color='#FFFF00'>v{0}</font></font>"
}

en = {
    "titleOK": "\nUpdate - Press RESTART",
    "messageWAIT": "Wait while downloading Updates v{0}",
    "messageOK": "Click RESTART to complete the Upgrade process. v{0}",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Choose a download option.</b></font>\n"
        "<p align='left'><font color ='#00FF00'><b>Automatically</b></font> - download and unpack the archive"
        "updates to the folder {0}\n<font color='#FFFF00'><b>Manually</b></font> - will open a link to"
        "the same archive, but you will have to extract the package and copy the *.wotmod file manually.</p>"
        "\n<font size='20 'color='#FFFF00'><b>Changelog</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "\n<font size='20'>Update available <font color='#FFFF00'>v{0}</font></font>"
}

uk = {
    "titleOK": "\nОновлення готове",
    "messageWAIT": "Зачекайте, будь ласка, йде завантаження оновлення v{0}",
    "messageOK": "Нажміть ПЕРЕЗАВАНТАЖЕННЯ для завершення процесу оновлення. v{0}",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Выберіть варіант завантаження.</b></font>\n"
        "<p align='left'><font color='#00FF00'><b>Автоматично</b></font> - завантажить і розпакує архів "
        "оновлення в папку. {0}\n<font color='#FFFF00'><b>Вручну</b></font> - відкриє в браузері посилання на "
        "цей же архів, але витягувати пакет і копіювати *.wotmod файли потрібно буде в ручному режимі.</p>"
        "\n<font size='20' color='#FFFF00'><b>Список змін</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "\n<font size='20'>Доступне оновлення <font color='#FFFF00'>v{0}</font></font>"
}


def getI18n():
    if getClientLanguage().lower() == 'uk':
        return ru
    elif getClientLanguage().lower() in ('ru', 'uk', 'be'):
        return ru
    else:
        return en
