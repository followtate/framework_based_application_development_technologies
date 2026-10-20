"""Класс Category и функции работы с категориями."""

from __future__ import annotations

from .sources import Source


class Category:
    """Тематическая группа источников."""

    def __init__(
        self,
        category_id: int,
        name: str,
        description: str = "",
    ) -> None:
        """Создать категорию."""
        self.id = category_id
        self.name = name
        self.description = description
        self.sources: list[Source] = []

    @property
    def source_count(self) -> int:
        """Количество источников в категории."""
        return len(self.sources)

    @classmethod
    def from_data(
        cls,
        data: dict,
        sources_by_id: dict[int, "Source"],
    ) -> "Category":
        """Восстановить категорию из данных JSON."""
        category = cls(
            category_id=int(data["id"]),
            name=data["name"],
            description=data.get("description", ""),
        )
        for source_id in data.get("source_ids", []):
            source = sources_by_id.get(int(source_id))
            if source is not None:
                category.sources.append(source)
        return category

    def to_dict(self) -> dict:
        """Преобразовать категорию в структуру для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "source_ids": [source.id for source in self.sources],
        }

    def add_source(self, source: "Source") -> bool:
        """Добавить источник в категорию; вернуть True, если добавлен."""
        if any(existing.id == source.id for existing in self.sources):
            return False
        self.sources.append(source)
        return True

    def __str__(self) -> str:
        description = self.description or "—"
        return (
            f"{self.name} ({description}), "
            f"источников: {self.source_count}"
        )


def next_id(categories: dict[int, "Category"]) -> int:
    """Следующий свободный идентификатор категории."""
    return max(categories, default=0) + 1


def create_category(
    categories: dict[int, "Category"],
    name: str,
    description: str = "",
) -> "Category":
    """Создать категорию и добавить её в коллекцию."""
    name = name.strip()
    description = description.strip()

    if not name:
        raise ValueError("Название категории не может быть пустым")

    for category in categories.values():
        if category.name.lower() == name.lower():
            raise ValueError("Категория с таким названием уже существует")

    category = Category(
        category_id=next_id(categories),
        name=name,
        description=description,
    )
    categories[category.id] = category
    return category


def get_category(
    categories: dict[int, "Category"],
    category_id: int,
) -> "Category":
    """Получить категорию по идентификатору."""
    try:
        return categories[category_id]
    except KeyError as exc:
        raise KeyError(
            f"Категория с id={category_id} не найдена"
        ) from exc


def list_categories(
    categories: dict[int, "Category"],
) -> list["Category"]:
    """Вернуть список категорий."""
    return list(categories.values())