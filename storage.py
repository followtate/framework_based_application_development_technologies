"""Сохранение и загрузка данных проекта в JSON."""

import json
from pathlib import Path
from typing import Any

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
        print(f"[ОШИБКА] Файл {path.name} повреждён. Данные не загружены.")
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


def _int_keys(data: dict[str, dict]) -> dict[int, dict]:
    """Преобразовать строковые ключи JSON в целочисленные id."""
    if not isinstance(data, dict):
        return {}

    result: dict[int, dict] = {}
    for key, value in data.items():
        try:
            result[int(key)] = value
        except ValueError:
            continue
    return result


def load_data() -> tuple[
    dict[str, dict],
    dict[int, dict],
    dict[int, dict],
    dict[int, dict],
]:
    """Загрузить пользователей, источники, категории и списки."""
    users = _load_json(USERS_FILE, {})
    sources = _int_keys(_load_json(SOURCES_FILE, {}))
    categories = _int_keys(_load_json(CATEGORIES_FILE, {}))
    reading_lists = _int_keys(_load_json(LISTS_FILE, {}))
    return users, sources, categories, reading_lists


def save_data(
    users: dict[str, dict],
    sources: dict[int, dict],
    categories: dict[int, dict],
    reading_lists: dict[int, dict],
) -> None:
    """Сохранить все данные проекта."""
    _save_json(USERS_FILE, users)
    _save_json(SOURCES_FILE, sources)
    _save_json(CATEGORIES_FILE, categories)
    _save_json(LISTS_FILE, reading_lists)
