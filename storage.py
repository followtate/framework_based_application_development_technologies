"""Сохранение и загрузка данных в JSON."""

import json
from pathlib import Path
from typing import Any

from models import Category, ReadingList, Source, User

DATA_DIR = Path(__file__).resolve().parent / "data"
USERS_FILE = DATA_DIR / "users.json"
SOURCES_FILE = DATA_DIR / "sources.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"
LISTS_FILE = DATA_DIR / "reading_lists.json"


def _load_json(path: Path, default: Any) -> Any:
    """Прочитать JSON-файл; при ошибке вернуть значение по умолчанию."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(
            f"[ОШИБКА] Файл {path.name} повреждён. "
            f"Данные не загружены."
        )
        return default
    except OSError as exc:
        print(f"[ОШИБКА] Не удалось прочитать {path.name}: {exc}")
        return default


def _save_json(path: Path, data: Any) -> None:
    """Записать данные в JSON-файл через контекстный менеджер."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"[ОШИБКА] Не удалось сохранить {path.name}: {exc}")


def load_users() -> dict[str, User]:
    """Загрузить пользователей из users.json."""
    raw = _load_json(USERS_FILE, {})
    users: dict[str, User] = {}
    if not isinstance(raw, dict):
        return users
    for login, data in raw.items():
        try:
            user = User.from_data(data)
            users[login] = user
        except (KeyError, TypeError, ValueError):
            continue
    return users


def load_sources() -> dict[int, Source]:
    """Загрузить источники из sources.json."""
    raw = _load_json(SOURCES_FILE, {})
    sources: dict[int, Source] = {}
    if not isinstance(raw, dict):
        return sources
    for data in raw.values():
        try:
            source = Source.from_data(data)
            sources[source.id] = source
        except (KeyError, TypeError, ValueError):
            continue
    return sources


def load_categories(
    sources: dict[int, Source],
) -> dict[int, Category]:
    """Загрузить категории с восстановлением ссылок на источники."""
    raw = _load_json(CATEGORIES_FILE, {})
    categories: dict[int, Category] = {}
    if not isinstance(raw, dict):
        return categories
    for data in raw.values():
        try:
            category = Category.from_data(data, sources)
            categories[category.id] = category
        except (KeyError, TypeError, ValueError):
            continue
    return categories


def load_reading_lists(
    users: dict[str, User],
    sources: dict[int, Source],
    categories: dict[int, Category],
) -> dict[int, ReadingList]:
    """Загрузить списки с восстановлением связей с User/Source/Category."""
    raw = _load_json(LISTS_FILE, {})
    reading_lists: dict[int, ReadingList] = {}
    if not isinstance(raw, dict):
        return reading_lists
    for data in raw.values():
        try:
            reading_list = ReadingList.from_data(
                data, users, sources, categories
            )
            if reading_list is not None:
                reading_lists[reading_list.id] = reading_list
        except (KeyError, TypeError, ValueError):
            continue
    return reading_lists


def load_data() -> tuple[
    dict[str, User],
    dict[int, Source],
    dict[int, Category],
    dict[int, ReadingList],
]:
    """Загрузить все данные проекта и восстановить объекты."""
    users = load_users()
    sources = load_sources()
    categories = load_categories(sources)
    reading_lists = load_reading_lists(users, sources, categories)
    return users, sources, categories, reading_lists


def save_data(
    users: dict[str, User],
    sources: dict[int, Source],
    categories: dict[int, Category],
    reading_lists: dict[int, ReadingList],
) -> None:
    """Сохранить все объекты проекта в JSON."""
    _save_json(
        USERS_FILE,
        {login: user.to_dict() for login, user in users.items()},
    )
    _save_json(
        SOURCES_FILE,
        {
            str(source.id): source.to_dict()
            for source in sources.values()
        },
    )
    _save_json(
        CATEGORIES_FILE,
        {
            str(category.id): category.to_dict()
            for category in categories.values()
        },
    )
    _save_json(
        LISTS_FILE,
        {
            str(rl.id): rl.to_dict()
            for rl in reading_lists.values()
        },
    )