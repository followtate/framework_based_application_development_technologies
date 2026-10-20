"""Функции работы со списками литературы."""

from categories import add_source_to_category
from sources import get_source
from utils import next_id, now_iso

ALLOWED_READING_STATUSES = {"не начат", "в процессе", "прочитан"}


def create_list(
    reading_lists: dict[int, dict],
    title: str,
    owner_login: str,
) -> dict:
    """Создать пользовательский список литературы."""
    title = title.strip()
    owner_login = owner_login.strip()

    if not title:
        raise ValueError("Название списка не может быть пустым")
    if not owner_login:
        raise ValueError("Владелец списка не указан")

    list_id = next_id(reading_lists)
    reading_list = {
        "id": list_id,
        "title": title,
        "owner": owner_login,
        "created_at": now_iso(),
        "items": [],
        "status": "активен",
    }
    reading_lists[list_id] = reading_list
    return reading_list


def get_list(reading_lists: dict[int, dict], list_id: int) -> dict:
    """Получить список по идентификатору."""
    try:
        return reading_lists[list_id]
    except KeyError as exc:
        raise KeyError(f"Список с id={list_id} не найден") from exc


def add_source_to_list(
    reading_lists: dict[int, dict],
    sources: dict[int, dict],
    categories: dict[int, dict],
    list_id: int,
    source_id: int,
    category_id: int | None = None,
) -> dict:
    """Добавить источник в список с проверкой дублирования."""
    reading_list = get_list(reading_lists, list_id)
    get_source(sources, source_id)

    for item in reading_list["items"]:
        if item["source_id"] == source_id:
            raise ValueError("Этот источник уже есть в списке")

    if category_id is not None:
        add_source_to_category(categories, category_id, source_id)

    entry = {
        "source_id": source_id,
        "category_id": category_id,
        "status": "не начат",
    }
    reading_list["items"].append(entry)
    return reading_list


def change_reading_status(
    reading_lists: dict[int, dict],
    list_id: int,
    source_id: int,
    new_status: str,
) -> dict:
    """Изменить статус чтения источника в списке."""
    new_status = new_status.strip().lower()
    if new_status not in ALLOWED_READING_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_READING_STATUSES))
        raise ValueError(f"Недопустимый статус. Разрешены: {allowed}")

    reading_list = get_list(reading_lists, list_id)
    for item in reading_list["items"]:
        if item["source_id"] == source_id:
            item["status"] = new_status
            return reading_list

    raise ValueError("Источник не найден в указанном списке")


def list_reading_lists(
    reading_lists: dict[int, dict],
    owner_login: str | None = None,
) -> list[dict]:
    """Вернуть списки, при необходимости отфильтрованные по владельцу."""
    if owner_login is None:
        return list(reading_lists.values())

    owner_login = owner_login.strip()
    return [
        reading_list
        for reading_list in reading_lists.values()
        if reading_list["owner"] == owner_login
    ]


def build_list_view(
    reading_lists: dict[int, dict],
    sources: dict[int, dict],
    categories: dict[int, dict],
    list_id: int,
) -> list[dict]:
    """Собрать строки содержимого списка с данными источника."""
    reading_list = get_list(reading_lists, list_id)
    rows: list[dict] = []

    for item in reading_list["items"]:
        source = get_source(sources, item["source_id"])
        category_name = "без категории"
        category_id = item.get("category_id")

        if category_id is not None and category_id in categories:
            category_name = categories[category_id]["name"]

        rows.append(
            {
                "source_id": source["id"],
                "title": source["title"],
                "author": source["author"],
                "year": source["year"],
                "type": source["type"],
                "category": category_name,
                "status": item["status"],
            }
        )

    return rows
