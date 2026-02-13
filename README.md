## 📦 Downloads / Завантаження

* [📥 Download the Latest Release / Завантажити останню версію](https://github.com/Armagomen/battle_observer/releases/latest/)

---

## 🌐 Official Resources / Офіційні ресурси

* [💬 DISCORD](https://discord.gg/Nma5T5snKW)
* [🎮 WG_MODS](https://wgmods.net/6811/)

---

## 🌐 Supported Languages / Підтримувані мови

- Ukrainian / Українська
- English / Англійська
- German / Німецька
- Polish / Польська
- Russian / Російська

---

## 🛡 Interface and Battle Statistics / Покращення інтерфейсу та бойової статистики

1. Display of team health (HP of individual tanks + strength difference)  
   Відображення здоров’я команд (HP окремих танків + різниця сил)

2. Log of dealt and received damage  
   Журнал завданої та отриманої шкоди

3. Counter of active and destroyed tanks  
   Лічильник активних і знищених танків

4. Updated PING and FPS panels  
   Оновлені панелі затримки PING та FPS

5. Customizable battle timer  
   Налаштування таймера бою

6. Player stats in battle (WG rating only)  
   Статистика гравців у бою (лише рейтинг WG)

7. Modified base capture indicators  
   Модифіковані індикатори захоплення бази

8. Damage counter for “High Caliber” medal  
   Лічильник шкоди для медалі «Основний калібр»

9. Display of your tank's HP in a visible spot  
   Відображення HP вашого танка у помітному місці

10. Highlighting players with hidden names in team lists  
    Підсвічування гравців з прихованими іменами у списках команд

11. Clock in garage and battle  
    Годинник у гаражі та бою

---

## 🎯 Camera, Aiming, and Visual Settings / Камера, приціл та візуальні налаштування

1. Dynamic camera zoom based on distance  
   Динамічне наближення камери залежно від дистанції

2. Maximum camera distance  
   Максимальна відстань для камери

3. Projectile flight time indicator  
   Індикатор часу польоту снаряда

4. Improved aiming circle and server reticle (size, stabilization timer)  
   Покращене коло прицілювання та серверний приціл (розміри, таймер стабілізації)

5. Centering the minimap via hotkey + info about destroyed tanks (icon/name)  
   Центрування мінімапи через гарячу клавішу + інформація про знищені танки (іконка/ім’я)

6. Customization of icons in team lists (brightness, color)  
   Налаштування іконок у списках команд (яскравість, кольори)

7. Armor calculator: actual thickness + reticle color change  
   Калькулятор броні: фактична товщина + зміна кольору прицілу

8. Distance to the nearest spotted enemy (no direction)  
   Відстань до найближчого поміченого ворога (без напрямку)

9. Disable effects: shaking, flashes, blackout in sniper mode  
   Вимкнення ефектів: тремтіння, спалахи, затемнення в снайперському режимі

10. Disable commander voiceovers  
    Вимкнення озвучки командира

11. Auto-exit sniper mode after firing (optional)  
    Автоматичний вихід із снайперського режиму після пострілу (за бажанням)

12. Customization of “Sixth Sense” icon (timer, animation, image)  
    Налаштування іконки «Шостого чуття» (таймер, анімація, зображення)

---

## ⚙️ Team, System, and Utility Features / Командні, системні та допоміжні функції

1. Auto-clear game cache on exit  
   Автоматичне очищення кешу гри при виході

2. Highlighting friends/clanmates in team lists with a special symbol  
   Підсвічування друзів/кланових гравців у списках команд спеціальним символом

3. Message filtering in system chat  
   Фільтрація повідомлень у системному чаті

4. Check slot availability for map blacklist  
   Перевірка наявності слоту для блокування мапи

5. Tank performance widget in garage (damage, spotting, blocking, stun, gun mark progress)  
   Віджет ефективності танка у гаражі (шкода, розвідка, блокування, оглушення, відсоток позначки на гарматі)

6. Auto-toggle “accelerated crew training” based on field modifications  
   Автоматичне перемикання «прискореного навчання екіпажу» залежно від польових модифікацій

7. Auto-collection of clan rewards  
   Автоматичне отримання кланових нагород

8. Disable base capture siren  
   Вимкнення сигналу захоплення бази

9. Disable elite widgets  
   Вимкнення віджетів елітності

---

## 💀 Post-Destruction Modes / Режими після знищення

1. Camera fixates on the final position after death  
   Після загибелі камера фіксується на останньому відомому положенні

2. Adjust camera distance after being destroyed  
   Корекція дистанції камери після знищення

---

## 🛠️ Формат макросів

<details>
<summary>Докладніше</summary>

#### Формат макросів:

```
%[(ім'я)][прапори][розмір][.точність]тип (без квадратних дужок) - %(macrosName)s, %(macrosName).10s
```

#### Додаткова інформація налаштування макросів.

````
Для зміни формату чисел потрібно редагувати лише кінцівку та ім'я макросу, %(макрос)s
замінити s на d - десяткове ціле число, на .Nf - число з плаваючою точкою де N(число) у знаків після точки.
Усі доступні макроси прописані нижче.
ВАЖЛИВО: щоб написати знак % який буде виводиться на екран і нічого не зламалося необхідно написати його двічі
Приклад: %(percent)d%% результатом виведення макросу буде 56%
````

#### Приклади форматування числових макросів:

```
Наприклад, у нас є число 234.56789
%(макрос)s - видасть число без змін, як дає пітон. результат = 234.56789
s - застосовується всім макросів за умовчанням.
Якщо результатом макросу є НЕ число, значення міняти НЕ МОЖНА.
В іншому випадку помилка в пітон лозі і мод працювати не буде.
Наступні приклади можна застосовувати лише до числових значень.
%(макрос)d - результат = 234
%(макрос).1f - результат = 234.6
%(макрос).2f - результат = 234.57
```

#### [Як форматувати текс](https://help.adobe.com/ru_RU/FlashPlatform/reference/actionscript/3/flash/text/TextField.html#htmlText)

#### [Як форматувати дату та час](https://docs.python.org/2/library/time.html#time.strftime)

#### Макроси для детальних логів шкоди:

`````
%(index)s           | порядковий номер.
%(shots)s           | Кількість влучень із втратою
%(totalDamage)s     | всього отримано від танка супротивника / нанесено танку супротивника
%(lastDamage)s      | Останній вистріл
%(allDamages)s      | Список всіх пострілів через кому 100, 23, 455, ..
%(classIcon)s       | іконка класу техніки
%(tankName)s        | назва танку
%(userName)s        | нік гравця
%(TankLevel)s       | рівень танка
%(tankClassColor)s  | колір класу техніки
%(attackReason)s    | тип атаки.
%(killedIcon)s      | іконка знищеного / кілера (для вхідного лога)
%(shellType)s       | Тип снаряду
%(shellColor)s      | Снаряди: золото/срібло
%(%DamageAvgColor)s | Динамічний колір нанесеної шкоди по співвідношенню ненесено/повне хп вашого танка.
`````

#### Макроси TOP лога:

`````
%(playerDamage)s       | Нанесений особисто
%(damageIcon)s         | Нанесений особисто значок
%(blockedDamage)s      | Заблокований бронею
%(blockedIcon)s        | Заблокований бронею значок
%(assistDamage)s       | Нанесений за вашою допомогою
%(assistIcon)s         | Нанесений за допомогою значок
%(spottedTanks)s       | Кількість виявлених танків
%(spottedIcon)s        | Кількість виявлених танків значок
%(stunIcon)s           | Нанесений на ваше оглушення іконка
%(stun)s               | Нанесений на ваше оглушення
%(tankDamageAvgColor)s | Динамічний колір нанесеної шкоди
%(tankAssistAvgColor)s | Динамічний колір збитків по розвідданим
%(tankBlockedAvgColor)s| Динамічний колір заблокованої шкоди
%(tankStunAvgColor)s   | Динамічний колір Оглушення
%(tankAvgDamage)s      | ваша середня завдана шкода
%(tankAvgAssist)s      | ваша середня шкода за розвідданими
%(tankAvgStun)s        | ваш середній крон із оглушення
%(tankAvgBlocked)s     | ваша середня заблокована шкода
`````

#### Макроси для таймера:

````
%(timer)s              | таймер
%(timerColor)s         | колір таймера
````

#### Міцність гравців у вухах:

````
%(health)d             | поточна міцність
%(maxHealth)d          | максимальна міцність
%(percent)d            | поточний відсоток
````

#### Шкода гравців у вухах:

````
%(damage)s             | выводе поточну шкоду гравця якшо вона більше нуля
````

#### Макроси статистики WGR:

`````
%(winRate).2f | відсоток перемог (округлення, дивись у прикладах форматування числових макросів)
%(colorWGR)s  | колір статистики
%(WGR)s       | статистика WGR
%(battles)s   | кількість боїв у форматі 1K 1.23K 25.5K
%(nickname)s  | нік гравця
%(clanTag)s   | тег клану, якщо є.
`````

</details>