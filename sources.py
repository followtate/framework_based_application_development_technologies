"""Функции работы с источниками."""

from datetime import date
from typing import Iterator

from utils import next_id

ALLOWED_SOURCE_TYPES = {"книга", "статья", "ссылка"}


def add_source(
    sources: dict[int, dict],
    title: str,
    author: str,
    year: int,
    source_type: str,
) -> dict:
    """Добавить источник и вернуть его карточку."""
    title = title.strip()
    author = author.strip()
    source_type = source_type.strip().lower()

    if not title:
        raise ValueError("Название источника не может быть пустым")
    if year < 0 or year > date.today().year + 1:
        raise ValueError("Некорректный год издания")
    if source_type not in ALLOWED_SOURCE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_SOURCE_TYPES))
        raise ValueError(
            f"Недопустимый тип источника. Разрешены: {allowed}"
        )

    source_id = next_id(sources)
    source = {
        "id": source_id,
        "title": title,
        "author": author,
        "year": int(year),
        "type": source_type,
    }
    sources[source_id] = source
    return source


def get_source(sources: dict[int, dict], source_id: int) -> dict:
    """Получить источник по идентификатору."""
    try:
        return sources[source_id]
    except KeyError as exc:
        raise KeyError(f"Источник с id={source_id} не найден") from exc


def find_sources(sources: dict[int, dict], query: str) -> list[dict]:
    """Найти источники по подстроке в названии или авторе."""
    query = query.strip().lower()
    if not query:
        return list(sources.values())

    return [
        source
        for source in sources.values()
        if query in source["title"].lower()
        or query in source["author"].lower()
    ]


def filter_sources_by_type(
    sources: dict[int, dict],
    source_type: str,
) -> Iterator[dict]:
    """Вернуть генератор источников заданного типа."""
    source_type = source_type.strip().lower()
    for source in sources.values():
        if source["type"] == source_type:
            yield source


def sort_sources(
    sources: dict[int, dict],
    key: str = "title",
    reverse: bool = False,
) -> list[dict]:
    """Отсортировать источники по title, author или year."""
    allowed = {"title", "author", "year"}
    if key not in allowed:
        raise ValueError("Сортировка возможна по title, author или year")

    return sorted(
        sources.values(),
        key=lambda source: source[key],
        reverse=reverse,
    )


def list_sources(sources: dict[int, dict]) -> list[dict]:
    """Вернуть все источники."""
    return list(sources.values())
