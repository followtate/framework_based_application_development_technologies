# Сервис управления списками литературы — веб-версия на Django

Учебный проект по дисциплине «Технологии разработки приложений на базе
фреймворков». Развивается поэтапно: консольное приложение на Python (ПР1–ПР3),
веб-интерфейс на Django (ПР5) и Django-шаблоны со статикой (ПР6).

1. Назначение

Приложение для ведения библиографии и списков чтения: источники (книги,
статьи, ссылки), тематические категории, пользовательские списки литературы
с отметкой статуса чтения. В ПР6 веб-интерфейс проекта переведён с
формирования HTML в Python на систему шаблонов Django.

2. Используемые технологии

- Python 3.10+;
- Django 5.2;
- Django Template Language (DTL);
- HTML5;
- CSS3, Bootstrap 5.3 (CDN);
- Bootstrap Icons (CDN);
- Bootstrap JS bundle (CDN);
- Google Fonts, Inter (CDN);
- собственные CSS, JavaScript, логотип через `{% static %}`;
- JSON — хранилище данных (Django ORM пока не используется);
- pytest, flake8;
- Git.

3. Предметная область

Четыре сущности (классы предметной области из ПР3):

- **User** — пользователь-владелец списков: `id`, `full_name`, `email`,
  `login`, `registered_at`;
- **Source** — источник: `id`, `title`, `author`, `year`, `type`
  (книга / статья / ссылка);
- **Category** — тематическая категория: `id`, `name`, `description`,
  `sources`;
- **ReadingList** — список литературы: `id`, `title`, `owner` (объект `User`),
  `items` (записи с `source`, `category`, `status`), `status`, `created_at`.

Сущности реализованы как Python-классы в пакете `models/`. Веб-слой использует
их напрямую, без дублирования логики. Данные хранятся в JSON-файлах
(`data/*.json`), Django ORM пока не используется.

4. Структура проекта

framework_based_applications_for_uni/
├── core/ # настройки Django
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
├── homepage/
│ ├── urls.py # app_name = "homepage"
│ ├── views.py # index, page_not_found
│ ├── templates/homepage/
│ │ └── index.html
│ └── static/homepage/
│ ├── css/style.css
│ ├── js/main.js
│ └── img/logo.svg
├── sources/
│ ├── urls.py # app_name = "sources"
│ ├── views.py # sources_list, source_detail
│ └── templates/sources/
│ ├── source_list.html
│ ├── source_detail.html
│ └── includes/source_card.html
├── categories/
│ ├── urls.py # app_name = "categories"
│ ├── views.py # categories_list
│ └── templates/categories/
│ └── category_list.html
├── reading_lists/
│ ├── urls.py # app_name = "lists"
│ ├── views.py # lists, list_detail
│ └── templates/reading_lists/
│ ├── list_list.html
│ ├── list_detail.html
│ └── includes/status_badge.html
├── templates/ # шаблоны уровня проекта
│ ├── base.html
│ ├── 404.html
│ └── includes/navigation.html
├── models/ # классы предметной области (ПР3)
│ ├── users.py
│ ├── sources.py
│ ├── categories.py
│ └── lists.py
├── data/ # JSON-хранилище
│ ├── users.json
│ ├── sources.json
│ ├── categories.json
│ └── reading_lists.json
├── tests/ # pytest
│ ├── test_users.py
│ ├── test_sources.py
│ ├── test_categories.py
│ └── test_lists.py
├── storage.py # JSON → объекты
├── utils.py # безопасный ввод (консоль)
├── main.py # консольная версия (ПР3)
├── manage.py
├── requirements.txt
├── setup.cfg # настройки flake8
└── README.md

5. Веб-интерфейс

Двухуровневая маршрутизация: корневой `core/urls.py` подключает маршруты
приложений через `include()`, в каждом приложении — свой `urls.py`
с `app_name` и `name=` у маршрутов.

| URL                         | View-функция                       | Шаблон                           |
| --------------------------- | ---------------------------------- | -------------------------------- |
| `/`                         | `homepage.views.index`             | `homepage/index.html`            |
| `/sources/`                 | `sources.views.sources_list`       | `sources/source_list.html`       |
| `/sources/<int:source_id>/` | `sources.views.source_detail`      | `sources/source_detail.html`     |
| `/categories/`              | `categories.views.categories_list` | `categories/category_list.html`  |
| `/lists/`                   | `reading_lists.views.lists`        | `reading_lists/list_list.html`   |
| `/lists/<int:list_id>/`     | `reading_lists.views.list_detail`  | `reading_lists/list_detail.html` |

Для динамических адресов используются конвертеры `<int:source_id>`
и `<int:list_id>`: идентификатор передаётся в view-функцию параметром.

Обработка ошибки 404 настроена через
`handler404 = "homepage.views.page_not_found"` в `core/urls.py` и шаблон
`templates/404.html`. View-функции для несуществующих объектов возвращают
ответ со статусом 404.

6. Django Template Language

HTML вынесен из Python-кода в `.html`-файлы. Функция `page()` из ПР5 удалена:
view-функции готовят контекст и вызывают `render()`, разметку формирует шаблон.

Используются:

- **`{% extends "base.html" %}`** — наследование общей структуры;
- **`{% block title %}` / `{% block content %}`** — переопределяемые блоки;
- **`{% include %}`** — переиспользуемые фрагменты:
  `includes/navigation.html`, `sources/includes/source_card.html`,
  `reading_lists/includes/status_badge.html`;
- **`{% for %}...{% empty %}`** — циклы с обработкой пустых коллекций;
- **`{% if %}` / `{% elif %}` / `{% else %}`** — условное отображение;
- **`{% url 'namespace:name' %}`** — ссылки через именованные маршруты;
- **фильтры `|length`** (количество источников, списков, категорий)
  и **`|default`** (значение по умолчанию).

Контекст передаётся из view в шаблон словарём:

```python
context = {"sources": list(sources.values())}
return render(request, "sources/source_list.html", context)

7. Статические файлы

Собственные статические файлы проекта находятся в
homepage/static/homepage/:

css/style.css — собственные стили (карточки с hover-эффектом, статусы,
логотип в навбаре);
js/main.js — вывод текущего года в футер;
img/logo.svg — логотип проекта.
Подключение в base.html через {% load static %} и
{% static 'homepage/...' %}. Bootstrap 5.3 и Bootstrap Icons подключены
через CDN и дополнены собственными стилями.

8. Хранение данных (ПР9: Django ORM)

Данные хранятся в реляционной БД SQLite (`db.sqlite3`), доступ — через
Django ORM. Модели описаны в `models.py` приложений `users`, `sources`,
`categories`, `reading_lists`. Миграции — в `*/migrations/`.

Модели и связи

- `users.User` — `login` (unique), `full_name`, `email`, `registered_at`;
- `sources.Source` — `title`, `author`, `year`, `type` (TextChoices:
  книга/статья/ссылка);
- `categories.Category` — `name`, `description`, `sources = M2M(Source,
  related_name="categories")`;
- `reading_lists.ReadingList` — `title`, `owner = FK(User,
  on_delete=CASCADE, related_name="reading_lists")`, `status`, `created_at`
  (от абстрактной `TimeStampedModel`);
- `reading_lists.ReadingListItem` — `reading_list = FK(ReadingList,
  on_delete=CASCADE, related_name="items")`, `source = FK(Source,
  on_delete=CASCADE, related_name="list_items")`, `category =
  FK(Category, on_delete=SET_NULL, null=True)`, `status` (TextChoices).


### ORM-запросы

Минимум 15 ORM-выражений реализовано в представлениях:
`all`, `get_object_or_404`, `filter`, `exclude`, `Q`, `order_by`,
`select_related`, `prefetch_related`, `aggregate`, `annotate`, `Count`,
`Paginator`. Подробный чек-лист — в отчёте по ПР9.
9. Запуск

Веб-версия (Django)

Из корня проекта, при активированном виртуальном окружении:

bash
source venv/bin/activate
python manage.py migrate
python manage.py check
python manage.py runserver
Открыть в браузере: http://127.0.0.1:8000/

10. Тесты

bash
python -m pytest -v
Тесты покрывают классы предметной области ПР3: пользователей, источники,
категории, списки литературы. Веб-слой (view-функции, шаблоны) тестами
пока не покрыт.

11. Проверка качества кода

bash
python -m flake8 . --extend-exclude=venv,migrations
Настройки flake8 — в setup.cfg (max-line-length = 99, исключены
venv/, migrations/, автогенерируемые admin.py, apps.py).

Проверка поиска статики:

bash
python manage.py findstatic homepage/css/style.css
python manage.py findstatic homepage/js/main.js
python manage.py findstatic homepage/img/logo.svg
12. Git

Каждый этап фиксируется коммитом с меткой практической работы:

bash
git add .
git commit -m "PR6: перевод веб-интерфейса на Django-шаблоны и статику"
git log --oneline
13. Текущее состояние и планы

Реализовано (ПР1–ПР6):

консольное приложение с объектной моделью (ПР3);
JSON-хранилище с загрузкой в объекты;
Django-проект и четыре приложения (ПР5);
двухуровневая маршрутизация с app_name и name;
view-функции с контекстом и render();
кастомная обработка 404 через handler404;
Django Template Language: extends, block, include, for, if,
empty, url, фильтры |length и |default;
базовый шаблон base.html, templates/includes/navigation.html;
собственные статические файлы: CSS, JS, логотип через {% static %};
pytest и flake8.
Не реализовано (планы на следующие работы):

Django ORM и реляционная база данных;
формы создания и редактирования объектов;
аутентификация и авторизация пользователей;
API;
тесты веб-слоя и шаблонов.
14. Ограничения этапа

Классы предметной области не наследуются от пользовательских базовых
классов: иерархия в предметной области не требует наследования,
композиция (ReadingList → User, Source, Category) полностью
покрывает связи.
Источник данных — JSON-файлы, а не БД. Переход на Django ORM — следующая
практическая работа.
DEBUG = True в settings.py — для разработки. Для проверки кастомной
страницы 404 временно выставить DEBUG = False и ALLOWED_HOSTS,
после проверки вернуть обратно.
```

## Django/SQLite-слой (ПР7)

Данные проекта перенесены из JSON-файлов в SQLite. Django-представления
получают результаты SQL-запросов через `sqlite3` (без Django ORM — это
следующий этап).

### Структура базы данных

- `users` — пользователи: `id`, `login`, `full_name`, `email`, `registered_at`;
- `sources` — источники: `id`, `title`, `author`, `year`, `type`;
- `categories` — категории: `id`, `name`, `description`;
- `category_sources` — связь M:N источник ↔ категория (`category_id`, `source_id`);
- `reading_lists` — списки литературы: `id`, `title`, `owner_id` (FK → `users.id`),
  `status`, `created_at`;
- `reading_list_items` — элементы списка: `id`, `reading_list_id` (FK),
  `source_id` (FK), `category_id` (FK, nullable), `status`.

Первичные ключи — `id` в каждой таблице. Внешние ключи включены через
`PRAGMA foreign_keys = ON`.

### Файлы

- `sql/schema.sql` — CREATE TABLE;
- `sql/queries.sql` — 12 SQL-запросов проекта (списки, WHERE, JOIN, агрегаты,
  GROUP BY, HAVING);
- `db/database.py` — подключение к SQLite с `row_factory = sqlite3.Row`;
- `db/import_json.py` — импорт данных из JSON в SQLite;
- `data/literature.sqlite` — файл базы данных.

### Страницы, использующие SQLite

- `/` — главная со статистикой из БД;
- `/sources/` — список источников (`ORDER BY title`);
- `/sources/<id>/` — карточка источника + категории (JOIN);
- `/sources/search/?q=...` — поиск по названию/автору (`LIKE`, параметризованный);
- `/sources/stats/` — статистика: источники по типам и категории по числу
  источников (GROUP BY + HAVING);
- `/lists/` — списки литературы с подсчётом элементов и прочитанных (GROUP BY);
- `/lists/<id>/` — содержимое списка (JOIN sources + categories);
- `/categories/` — категории с числом источников (LEFT JOIN + COUNT).

### Параметризованные запросы

Все значения, приходящие от пользователя (`source_id`, `list_id`, строка
поиска `q`), передаются через `?`, без f-строк и конкатенации.
