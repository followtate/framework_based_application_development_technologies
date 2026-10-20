"""Класс ReadingList и функции работы со списками литературы."""

from __future__ import annotations

from datetime import datetime

from .categories import Category
from .sources import Source
from .users import User


class ReadingList:
    """Пользовательский список литературы."""

    ALLOWED_STATUSES = {"не начат", "в процессе", "прочитан"}

    def __init__(
        self,
        list_id: int,
        title: str,
        owner: User,
    ) -> None:
        """Создать список литературы."""
        self.id = list_id
        self.title = title
        self.owner = owner
        self.items: list[dict] = []
        self.status = "активен"
        self.created_at = datetime.now().isoformat(timespec="seconds")

    @property
    def total_sources(self) -> int:
        """Всего источников в списке."""
        return len(self.items)

    @property
    def completed_sources(self) -> int:
        """Прочитанных источников."""
        return sum(
            1 for item in self.items
            if item["status"] == "прочитан"
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
        users_by_login: dict[str, User],
        sources_by_id: dict[int, Source],
        categories_by_id: dict[int, Category],
    ) -> "ReadingList | None":
        """Восстановить список литературы из данных JSON."""
        owner = users_by_login.get(data["owner"])
        if owner is None:
            return None

        reading_list = cls(
            list_id=int(data["id"]),
            title=data["title"],
            owner=owner,
        )
        reading_list.created_at = data.get(
            "created_at", reading_list.created_at
        )
        reading_list.status = data.get("status", "активен")

        for item_data in data.get("items", []):
            source = sources_by_id.get(int(item_data["source_id"]))
            if source is None:
                continue
            category = None
            category_id = item_data.get("category_id")
            if category_id is not None:
                category = categories_by_id.get(int(category_id))
            reading_list.items.append(
                {
                    "source": source,
                    "category": category,
                    "status": item_data.get("status", "не начат"),
                }
            )

        return reading_list

    def to_dict(self) -> dict:
        """Преобразовать список в структуру для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner.login,
            "items": [
                {
                    "source_id": item["source"].id,
                    "category_id": (
                        item["category"].id
                        if item["category"] is not None
                        else None
                    ),
                    "status": item["status"],
                }
                for item in self.items
            ],
            "status": self.status,
            "created_at": self.created_at,
        }

    def add_entry(
        self,
        source: Source,
        category: Category | None = None,
    ) -> bool:
        """Добавить источник в список; вернуть True, если добавлен."""
        if any(item["source"].id == source.id for item in self.items):
            return False
        self.items.append(
            {"source": source, "category": category, "status": "не начат"}
        )
        return True

    def change_status(self, source_id: int, new_status: str) -> bool:
        """Изменить статус чтения источника."""
        if new_status not in self.ALLOWED_STATUSES:
            allowed = ", ".join(sorted(self.ALLOWED_STATUSES))
            raise ValueError(
                f"Недопустимый статус. Разрешены: {allowed}"
            )
        for item in self.items:
            if item["source"].id == source_id:
                item["status"] = new_status
                return True
        return False

    def __str__(self) -> str:
        return (
            f"«{self.title}» — владелец: {self.owner.login}, "
            f"элементов: {self.total_sources}, "
            f"прочитано: {self.completed_sources}"
        )


def next_id(reading_lists: dict[int, "ReadingList"]) -> int:
    """Следующий свободный идентификатор списка."""
    return max(reading_lists, default=0) + 1


def create_list(
    reading_lists: dict[int, "ReadingList"],
    title: str,
    owner: User,
) -> "ReadingList":
    """Создать список литературы и добавить его в коллекцию."""
    title = title.strip()
    if not title:
        raise ValueError("Название списка не может быть пустым")

    reading_list = ReadingList(
        list_id=next_id(reading_lists),
        title=title,
        owner=owner,
    )
    reading_lists[reading_list.id] = reading_list
    return reading_list


def get_list(
    reading_lists: dict[int, "ReadingList"],
    list_id: int,
) -> "ReadingList":
    """Получить список по идентификатору."""
    try:
        return reading_lists[list_id]
    except KeyError as exc:
        raise KeyError(f"Список с id={list_id} не найден") from exc


def add_source_to_list(
    reading_lists: dict[int, "ReadingList"],
    list_id: int,
    source: Source,
    category: Category | None = None,
) -> "ReadingList":
    """Добавить источник в список с проверкой дублирования."""
    reading_list = get_list(reading_lists, list_id)
    if not reading_list.add_entry(source, category):
        raise ValueError("Этот источник уже есть в списке")
    if category is not None:
        category.add_source(source)
    return reading_list


def change_reading_status(
    reading_lists: dict[int, "ReadingList"],
    list_id: int,
    source_id: int,
    new_status: str,
) -> "ReadingList":
    """Изменить статус чтения источника в списке."""
    reading_list = get_list(reading_lists, list_id)
    if not reading_list.change_status(source_id, new_status):
        raise ValueError("Источник не найден в указанном списке")
    return reading_list


def list_reading_lists(
    reading_lists: dict[int, "ReadingList"],
    owner_login: str | None = None,
) -> list["ReadingList"]:
    """Вернуть списки, при необходимости отфильтрованные по владельцу."""
    if owner_login is None:
        return list(reading_lists.values())
    owner_login = owner_login.strip()
    return [
        reading_list
        for reading_list in reading_lists.values()
        if reading_list.owner.login == owner_login
    ]


def build_list_view(
    reading_lists: dict[int, "ReadingList"],
    list_id: int,
) -> list[dict]:
    """Собрать строки содержимого списка."""
    reading_list = get_list(reading_lists, list_id)
    rows: list[dict] = []
    for item in reading_list.items:
        rows.append(
            {
                "source_id": item["source"].id,
                "title": item["source"].title,
                "author": item["source"].author,
                "year": item["source"].year,
                "type": item["source"].type,
                "category": (
                    item["category"].name
                    if item["category"] is not None
                    else "без категории"
                ),
                "status": item["status"],
            }
        )
    return rows