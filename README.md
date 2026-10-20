# Сервис управления списками литературы (ООП-версия)

## Назначение

Приложение для ведения списков литературы: источники (книги, статьи, ссылки),
категории и пользовательские списки чтения. Реализовано в объектной модели Python.

## Возможности

- регистрация пользователя с проверкой email и уникальности логина;
- добавление источника (книга / статья / ссылка);
- создание категорий с привязкой источников;
- создание списка литературы, привязанного к объекту `User`;
- добавление источников в список с проверкой дублирования;
- изменение статуса чтения (`не начат`, `в процессе`, `прочитан`);
- поиск и фильтрация источников;
- сортировка источников через `lambda`;
- сохранение и загрузка данных в JSON;
- обработка некорректного ввода и ошибок файлов.

## Классы предметной области

### `User` — пользователь

Атрибуты: `id`, `full_name`, `email`, `login`, `registered_at`.
Методы: `__str__`, `validate_email()` (`@staticmethod`), `from_data()` (`@classmethod`), `to_dict()`.
Свойства: `display_name` (`@property`).

### `Source` — источник

Атрибуты: `id`, `title`, `author`, `year`, `type`.
Методы: `__str__`, `matches()`, `is_valid_year()` (`@staticmethod`), `is_allowed_type()` (`@staticmethod`), `from_data()` (`@classmethod`), `to_dict()`.

### `Category` — категория

Атрибуты: `id`, `name`, `description`, `sources: list[Source]`.
Методы: `__str__`, `add_source()`, `from_data()` (`@classmethod`), `to_dict()`.
Свойства: `source_count` (`@property`).

### `ReadingList` — список литературы

Атрибуты: `id`, `title`, `owner: User`, `items: list[dict]` (с `source: Source`, `category: Category | None`, `status: str`), `status`, `created_at`.
Методы: `__str__`, `add_entry()`, `change_status()`, `from_data()` (`@classmethod`), `to_dict()`.
Свойства: `total_sources`, `completed_sources` (`@property`).

## Взаимодействие объектов

```
ReadingList.owner  → User
ReadingList.items[i].source    → Source
ReadingList.items[i].category  → Category
Category.sources[i]            → Source
```

`ReadingList` связывает `User` с набором `Source` (через записи с категорией и статусом).
`Category` агрегирует `Source` по тематике.

## Архитектура

```
literature_service/
├── main.py               # консольное меню
├── storage.py            # JSON ↔ объекты
├── utils.py              # безопасный ввод
├── models/
│   ├── __init__.py
│   ├── users.py          # User + регистрация/поиск
│   ├── sources.py        # Source + поиск/фильтр/сортировка
│   ├── categories.py     # Category + создание/поиск
│   └── lists.py          # ReadingList + работа со списками
├── data/                 # JSON-хранилище
├── tests/                # pytest
├── setup.cfg             # настройки flake8
└── requirements.txt
```

## Формат данных

`data/users.json` — ключ — логин:

```json
{
  "ivan": {
    "id": 1,
    "full_name": "Иван Петров",
    "email": "ivan@example.com",
    "login": "ivan",
    "registered_at": "2026-10-20T12:00:00"
  }
}
```

`data/sources.json`:

```json
{
  "1": {
    "id": 1,
    "title": "Чистый код",
    "author": "Роберт Мартин",
    "year": 2008,
    "type": "книга"
  }
}
```

`data/categories.json`:

```json
{
  "1": {
    "id": 1,
    "name": "Программирование",
    "description": "Книги и статьи",
    "source_ids": [1]
  }
}
```

`data/reading_lists.json`:

```json
{
  "1": {
    "id": 1,
    "title": "Чтение на семестр",
    "owner": "ivan",
    "items": [{ "source_id": 1, "category_id": 1, "status": "не начат" }],
    "status": "активен",
    "created_at": "2026-10-20T12:00:00"
  }
}
```

При сохранении объектные ссылки (`ReadingList.owner`, `item["source"]`,
`item["category"]`, `Category.sources`) преобразуются в `login`/`id`.
При загрузке — обратно в объекты.

## Запуск

```bash
python3 main.py
```

## Тесты

```bash
python3 -m pytest -v
```

## Проверка качества кода

```bash
python3 -m flake8
```

## Ограничения

Проект использует только стандартную библиотеку Python 3.10+.
Классы не наследуются от пользовательских базовых классов: иерархия
в предметной области не требует наследования, а композиция
(`ReadingList` → `User`, `Source`, `Category`) полностью покрывает связи.
