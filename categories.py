"""Функции работы с категориями."""

from utils import next_id


def create_category(
    categories: dict[int, dict],
    name: str,
    description: str = "",
) -> dict:
    """Создать категорию и вернуть её карточку."""
    name = name.strip()
    description = description.strip()

    if not name:
        raise ValueError("Название категории не может быть пустым")

    for category in categories.values():
        if category["name"].lower() == name.lower():
            raise ValueError("Категория с таким названием уже существует")

    category_id = next_id(categories)
    category = {
        "id": category_id,
        "name": name,
        "description": description,
        "source_ids": [],
    }
    categories[category_id] = category
    return category


def get_category(categories: dict[int, dict], category_id: int) -> dict:
    """Получить категорию по идентификатору."""
    try:
        return categories[category_id]
    except KeyError as exc:
        raise KeyError(f"Категория с id={category_id} не найдена") from exc


def add_source_to_category(
    categories: dict[int, dict],
    category_id: int,
    source_id: int,
) -> dict:
    """Связать источник с категорией без дублирования."""
    category = get_category(categories, category_id)
    if source_id not in category["source_ids"]:
        category["source_ids"].append(source_id)
    return category


def list_categories(categories: dict[int, dict]) -> list[dict]:
    """Вернуть список категорий."""
    return list(categories.values())
