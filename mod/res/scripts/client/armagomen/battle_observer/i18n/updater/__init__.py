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
    "titleNEW": "<font size='20'>Update available <font color='#FFFF00'>v{0}</font></font>",
    "messages": (
        "Checking for an available update.",
        "The update check is completed, you have the current version.",
        "An update {} is detected, the client will be restarted at the end of the download.",
        "DownloadThread: downloading started: {} of {}",
        "DownloadThread: added new file {}",
        "DownloadThread: update is already downloaded to: {}",
        "DownloadThread: downloading update finished to: {}",
        "DownloadThread: downloading failed: {}"
    )
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
    "titleNEW": "<font size='20'>Доступне оновлення <font color='#FFFF00'>v{0}</font></font>",
    "messages": (
        "Перевірка доступного оновлення.",
        "Перевірка завершена — у вас актуальна версія.",
        "Виявлено оновлення {} — клієнт буде перезапущено після завершення завантаження.",
        "DownloadThread: завантаження запущено: {} з {}",
        "DownloadThread: додано новий файл {}",
        "DownloadThread: оновлення вже завантажене до: {}",
        "DownloadThread: завантаження завершено до: {}",
        "DownloadThread: збій завантаження: {}"
    )
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
    "titleNEW": "<font size='20'>Доступно обновление <font color='#FFFF00'>v{0}</font></font>",
    "messages": (
        "Проверка доступного обновления.",
        "Проверка завершена — у вас актуальная версия.",
        "Обнаружено обновление {} — клиент будет перезапущен после загрузки.",
        "DownloadThread: загрузка начата: {} из {}",
        "DownloadThread: добавлен новый файл {}",
        "DownloadThread: обновление уже загружено в: {}",
        "DownloadThread: загрузка завершена в: {}",
        "DownloadThread: сбой загрузки: {}"
    )
}

pl = {
    "titleOK": "Aktualizacja – naciśnij RESTART",
    "messageOK": "Kliknij „Zamknij grę”, aby zakończyć proces aktualizacji. v{0}\n",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Wybierz opcję pobierania.</b></font>\n"
        "<p align='left'><font color ='#00FF00'><b>Automatycznie</b></font> – pobierz i wypakuj archiwum"
        " z aktualizacją do folderu {0}\n<font color='#FFFF00'><b>Ręcznie</b></font> – otwiera link do instalatora w"
        " przeglądarce; instalacja ręczna będzie wymagana.</p>"
        "\n<font size='20' color='#FFFF00'><b>Lista zmian</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "<font size='20'>Dostępna aktualizacja <font color='#FFFF00'>v{0}</font></font>",
    "messages": (
        "Sprawdzanie dostępnej aktualizacji.",
        "Sprawdzanie zakończone – masz aktualną wersję.",
        "Wykryto aktualizację {} – klient zostanie ponownie uruchomiony po zakończeniu pobierania.",
        "DownloadThread: Rozpoczęto pobieranie: {} z {}",
        "DownloadThread: dodano nowy plik {}",
        "DownloadThread: aktualizacja już pobrana do: {}",
        "DownloadThread: pobieranie zakończone w: {}",
        "DownloadThread: pobieranie nie powiodło się: {}"
    )
}

de = {
    "titleOK": "Update – Neustart erforderlich",
    "messageOK": "Klicke auf „Spiel schließen“, um das Update abzuschließen. v{0}\n",
    "messageNEW":
        "<font size='15'>"
        "<font size='20' color='#FFFF00'><b>Wähle eine Download-Option.</b></font>\n"
        "<p align='left'><font color ='#00FF00'><b>Automatisch</b></font> – lade das Archiv herunter und entpacke"
        " es in den Ordner {0}\n<font color='#FFFF00'><b>Manuell</b></font> – öffnet den Link zum Installer im"
        " Browser; die Installation erfolgt manuell.</p>"
        "\n<font size='20' color='#FFFF00'><b>Änderungsprotokoll</b></font>\n"
        "<p align='left'>{1}</p>"
        "</font>",
    "titleNEW": "<font size='20'>Update verfügbar <font color='#FFFF00'>v{0}</font></font>",
    "messages": (
        "Suche nach verfügbaren Updates.",
        "Updateprüfung abgeschlossen – aktuelle Version installiert.",
        "Update {} erkannt – der Client wird nach dem Herunterladen neu gestartet.",
        "DownloadThread: Download gestartet: {} von {}",
        "DownloadThread: neue Datei hinzugefügt {}",
        "DownloadThread: Update bereits heruntergeladen in: {}",
        "DownloadThread: Download abgeschlossen in: {}",
        "DownloadThread: Download fehlgeschlagen: {}"
    )
}

LOCALIZED_BY_LANG = {
    "uk": uk,
    "ru": ru,
    "pl": pl,
    "de": de
}.get(getClientLanguage(), en)
