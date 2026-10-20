"""Класс Source и функции работы с источниками."""

from __future__ import annotations

from datetime import date
from typing import Iterator


class Source:
    """Источник — книга, статья или ссылка."""

    ALLOWED_TYPES = {"книга", "статья", "ссылка"}

    def __init__(
        self,
        source_id: int,
        title: str,
        author: str,
        year: int,
        source_type: str,
    ) -> None:
        """Создать объект источника."""
        self.id = source_id
        self.title = title
        self.author = author
        self.year = year
        self.type = source_type

    @staticmethod
    def is_valid_year(year: int) -> bool:
        """Проверить корректность года издания."""
        return 0 <= year <= date.today().year + 1

    @staticmethod
    def is_allowed_type(source_type: str) -> bool:
        """Проверить допустимость типа источника."""
        return source_type in Source.ALLOWED_TYPES

    @classmethod
    def from_data(cls, data: dict) -> "Source":
        """Восстановить источник из данных JSON."""
        return cls(
            source_id=int(data["id"]),
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            source_type=data["type"],
        )

    def to_dict(self) -> dict:
        """Преобразовать источник в структуру для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "type": self.type,
        }

    def matches(self, query: str) -> bool:
        """Проверить, встречается ли подстрока в названии или авторе."""
        q = query.strip().lower()
        return q in self.title.lower() or q in self.author.lower()

    def __str__(self) -> str:
        return f"{self.title} — {self.author} ({self.year}), {self.type}"


def next_id(sources: dict[int, "Source"]) -> int:
    """Следующий свободный идентификатор источника."""
    return max(sources, default=0) + 1


def add_source(
    sources: dict[int, "Source"],
    title: str,
    author: str,
    year: int,
    source_type: str,
) -> "Source":
    """Создать источник и добавить его в коллекцию."""
    title = title.strip()
    author = author.strip()
    source_type = source_type.strip().lower()

    if not title:
        raise ValueError("Название источника не может быть пустым")
    if not Source.is_valid_year(year):
        raise ValueError("Некорректный год издания")
    if not Source.is_allowed_type(source_type):
        allowed = ", ".join(sorted(Source.ALLOWED_TYPES))
        raise ValueError(
            f"Недопустимый тип источника. Разрешены: {allowed}"
        )

    source = Source(
        source_id=next_id(sources),
        title=title,
        author=author,
        year=int(year),
        source_type=source_type,
    )
    sources[source.id] = source
    return source


def get_source(sources: dict[int, "Source"], source_id: int) -> "Source":
    """Получить источник по идентификатору."""
    try:
        return sources[source_id]
    except KeyError as exc:
        raise KeyError(f"Источник с id={source_id} не найден") from exc


def find_sources(
    sources: dict[int, "Source"],
    query: str,
) -> list["Source"]:
    """Найти источники по подстроке в названии или авторе."""
    if not query.strip():
        return list(sources.values())
    return [source for source in sources.values() if source.matches(query)]


def filter_sources_by_type(
    sources: dict[int, "Source"],
    source_type: str,
) -> Iterator["Source"]:
    """Вернуть генератор источников заданного типа."""
    source_type = source_type.strip().lower()
    for source in sources.values():
        if source.type == source_type:
            yield source


def sort_sources(
    sources: dict[int, "Source"],
    key: str = "title",
    reverse: bool = False,
) -> list["Source"]:
    """Отсортировать источники по title, author или year."""
    allowed = {"title", "author", "year"}
    if key not in allowed:
        raise ValueError("Сортировка возможна по title, author или year")

    return sorted(
        sources.values(),
        key=lambda source: getattr(source, key),
        reverse=reverse,
    )


def list_sources(sources: dict[int, "Source"]) -> list["Source"]:
    """Вернуть все источники."""
    return list(sources.values())