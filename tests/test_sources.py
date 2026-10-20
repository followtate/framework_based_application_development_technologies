"""Тесты источников."""

import pytest

from models import Source
from models.sources import (
    add_source,
    filter_sources_by_type,
    find_sources,
    sort_sources,
)


def test_source_creation() -> None:
    source = Source(1, "Чистый код", "Роберт Мартин", 2008, "книга")
    assert source.id == 1
    assert source.title == "Чистый код"
    assert source.year == 2008
    assert source.type == "книга"


def test_source_str_and_matches() -> None:
    source = Source(1, "Чистый код", "Роберт Мартин", 2008, "книга")
    assert "Чистый код" in str(source)
    assert source.matches("чистый")
    assert source.matches("мартин")
    assert not source.matches("pep")


def test_source_from_data() -> None:
    data = {
        "id": 2,
        "title": "PEP 8",
        "author": "Guido",
        "year": 2001,
        "type": "статья",
    }
    source = Source.from_data(data)
    assert source.id == 2
    assert source.type == "статья"


def test_add_and_find_source() -> None:
    sources: dict[int, Source] = {}
    source = add_source(sources, "Чистый код", "Мартин", 2008, "книга")
    assert source.id == 1
    assert find_sources(sources, "чистый")[0] is source


def test_filter_by_type() -> None:
    sources: dict[int, Source] = {}
    add_source(sources, "Книга", "Автор", 2008, "книга")
    add_source(sources, "Статья", "Автор", 2020, "статья")
    found = list(filter_sources_by_type(sources, "статья"))
    assert len(found) == 1
    assert found[0].type == "статья"


def test_sort_sources() -> None:
    sources: dict[int, Source] = {}
    add_source(sources, "Б", "Автор", 2020, "книга")
    add_source(sources, "А", "Автор", 2021, "книга")
    sorted_sources = sort_sources(sources, "title")
    assert sorted_sources[0].title == "А"


def test_invalid_type() -> None:
    sources: dict[int, Source] = {}
    with pytest.raises(ValueError):
        add_source(sources, "Книга", "Автор", 2008, "журнал")