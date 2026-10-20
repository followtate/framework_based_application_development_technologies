"""Тесты источников."""

from sources import (
    add_source,
    filter_sources_by_type,
    find_sources,
    sort_sources,
)


def test_add_and_find_source() -> None:
    sources: dict[int, dict] = {}
    source = add_source(
        sources, "Чистый код", "Роберт Мартин", 2008, "книга"
    )
    assert source["id"] == 1
    assert find_sources(sources, "чистый")[0]["title"] == "Чистый код"


def test_filter_by_type() -> None:
    sources: dict[int, dict] = {}
    add_source(sources, "Книга", "Автор", 2008, "книга")
    add_source(sources, "Статья", "Автор", 2020, "статья")
    found = list(filter_sources_by_type(sources, "статья"))
    assert len(found) == 1


def test_sort_sources() -> None:
    sources: dict[int, dict] = {}
    add_source(sources, "Б", "Автор", 2020, "книга")
    add_source(sources, "А", "Автор", 2021, "книга")
    sorted_sources = sort_sources(sources, "title")
    assert sorted_sources[0]["title"] == "А"
