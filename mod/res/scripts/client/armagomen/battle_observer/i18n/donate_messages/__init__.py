# coding=utf-8
from armagomen._constants import IMG, URLS
from helpers import getClientLanguage

language = getClientLanguage()

MESSAGES = {
    "uk": (
        "Привіт, друзі! Якщо вам подобається наш контент, будь ласка, розгляньте можливість підтримати нас. Ваші донати допомагають нам створювати ще більше цікавого матеріалу!",
        "Вітаємо, команда! Наш проект зростає завдяки вам. Якщо ви хочете підтримати нас, перейдіть за посиланням в описі. Кожен донат важливий!",
        "Друзі, дякуємо вам за те, що залишаєтеся з нами! Якщо ви хочете допомогти розвитку нашого проекту, натисніть посилання. Ваша підтримка цінна для нас!"
    ),
    "pl": (
        "Cześć, przyjaciele! Jeśli podoba się Wam nasza treść, rozważcie wsparcie projektu. Wasze donacje pomagają nam tworzyć jeszcze więcej ciekawych materiałów!",
        "Witamy, ekipo! Nasz projekt rozwija się dzięki Wam. Jeśli chcecie nas wesprzeć, kliknijcie w link w opisie. Każda darowizna ma znaczenie!",
        "Dziękujemy, że jesteście z nami! Aby pomóc w rozwoju projektu, kliknijcie link – Wasze wsparcie jest dla nas bardzo ważne!"
    ),
    "de": (
        "Hallo Freunde! Wenn euch unsere Inhalte gefallen, erwägt bitte eine Unterstützung. Eure Spenden helfen uns, noch mehr spannende Beiträge zu erstellen!",
        "Willkommen, Team! Unser Projekt wächst dank euch. Wenn ihr uns unterstützen möchtet, klickt auf den Link in der Beschreibung. Jede Spende zählt!",
        "Danke, dass ihr dabei seid! Wenn ihr die Weiterentwicklung unseres Projekts fördern wollt, klickt auf den Link. Eure Unterstützung ist uns wichtig!"
    )
}.get(language, (
    "Hello, friends! If you enjoy our content, please consider supporting us. Your donations help us create even more interesting material!",
    "Congratulations, team! Our project is growing thanks to all of you. If you'd like to support us, click the link in the description. Every donation matters!",
    "Friends, thank you for staying with us! If you want to contribute to the development of our project, click the link. Your support means a lot to us!"
))

ONLINE = {
    "uk": "Онлайн користувачів: {}\nУсього користувачів: {}",
    "ru": "Онлайн пользователей: {}\nВсего пользователей: {}",
    "de": "Benutzer online: {}\nGesamtzahl der Benutzer: {}",
    "pl": "Użytkownicy online: {}\nŁączna liczba użytkowników: {}"
}.get(language, "Online users: {}\nTotal users: {}")

LINKS_FORMAT = {
    "uk": {"url": URLS.MONO, "img": IMG.MONO, "name": "MONO - поповнити банку."},
    "ru": {"url": URLS.MONO, "img": IMG.MONO, "name": "MONO - закинуть в банку."},
}.get(language, {"url": URLS.DONATELLO, "img": IMG.DONATELLO, "name": "DONATE - euro|uah|usdt."})
