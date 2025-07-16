# coding=utf-8

from helpers import getClientLanguage

language = getClientLanguage()

labels = {
    "uk": ("Закрити гру", "Автоматично", "Вручну", "Скасувати", "Закрити", "Застосувати",
           "Ігнорувати цей танк", "Так", "Ні"),
    "pl": ("Zamknij grę", "Automatycznie", "Ręcznie", "Anuluj", "Zamknij", "Zastosuj",
           "Ignoruj ten pojazd", "Tak", "Nie"),
    "de": ("Spiel schließen", "Automatisch", "Manuell", "Abbrechen", "Schließen", "Übernehmen",
           "Dieses Fahrzeug ignorieren", "Ja", "Nein"),
    "ru": ("Закрыть игру", "Автоматически", "Ручной режим", "Отменить", "Закрыть", "Применить",
           "Игнорировать танк", "Да", "Нет"),
}.get(language,
      ("Close game", "Automatically", "Manually", "Cancel", "Close", "Apply",
       "Ignore this tank", "Yes", "No"))

ban_info = {
    "uk": (
        "Доступ заборонено\n\nID: {}\nІм`я: {}\n\nВаш доступ до цієї послуги обмежено. "
        "Якщо ви вважаєте, що це помилка, або хочете оскаржити рішення, зверніться до служби підтримки, "
        "вказавши свій ідентифікатор користувача.\n\nДякуємо за розуміння."
    ),
    "pl": (
        "Dostęp zablokowany\n\nID: {}\nNazwa: {}\n\nTwój dostęp do tej usługi został ograniczony. "
        "Jeśli uważasz, że to pomyłka lub chcesz odwołać decyzję, skontaktuj się z pomocą techniczną, "
        "podając swój identyfikator użytkownika.\n\nDziękujemy za zrozumienie."
    ),
    "de": (
        "Zugriff verweigert\n\nID: {}\nName: {}\n\nDein Zugriff auf diesen Dienst wurde eingeschränkt. "
        "Falls du denkst, dass es sich um ein Versehen handelt oder du Einspruch einlegen möchtest, "
        "wende dich bitte an den Support und gib deine Benutzer-ID an.\n\nVielen Dank für dein Verständnis."
    ),
    "ru": (
        "Доступ запрещён\n\nID: {}\nИмя: {}\n\nВаш доступ к этой услуге ограничен. Если вы считаете, что это ошибка, "
        "или хотите обжаловать решение, обратитесь в службу поддержки, указав свой идентификатор пользователя.\n\nБлагодарим за понимание."
    ),
}.get(language,
      "Access Denied\n\nID: {}\nName: {}\n\nYour access to this service has been restricted. "
      "If you believe this is a mistake or would like to appeal the decision, please contact support with your User ID.\n\n"
      "Thank you for your understanding.")

error_template = {
    "uk": "Повідомлення про помилку: {}",
    "ru": "Сообщение об ошибке: {}",
    "pl": "Komunikat o błędzie: {}",
    "de": "Fehlermeldung: {}"
}.get(language, "Error message: {}")