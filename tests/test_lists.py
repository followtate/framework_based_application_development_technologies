"""Тесты списков литературы."""

import pytest

from models import Category, ReadingList, Source, User
from models.lists import (
    add_source_to_list,
    change_reading_status,
    create_list,
)


def _make_user() -> User:
    return User(1, "Иван", "ivan@example.com", "ivan")


def _make_source() -> Source:
    return Source(1, "Книга", "Автор", 2008, "книга")


def test_reading_list_creation() -> None:
    user = _make_user()
    reading_list = ReadingList(1, "Мой список", user)
    assert reading_list.id == 1
    assert reading_list.owner is user
    assert reading_list.total_sources == 0
    assert reading_list.completed_sources == 0


def test_reading_list_str() -> None:
    user = _make_user()
    reading_list = ReadingList(1, "Мой список", user)
    text = str(reading_list)
    assert "Мой список" in text
    assert "ivan" in text


def test_add_entry_and_duplicate() -> None:
    user = _make_user()
    source = _make_source()
    category = Category(1, "Наука")
    reading_list = ReadingList(1, "Мой список", user)

    assert reading_list.add_entry(source, category)
    assert not reading_list.add_entry(source, category)
    assert reading_list.total_sources == 1
    assert source.id in {s.id for s in category.sources}


def test_change_status() -> None:
    user = _make_user()
    source = _make_source()
    reading_list = ReadingList(1, "Мой список", user)
    reading_list.add_entry(source)

    assert reading_list.change_status(source.id, "прочитан")
    assert reading_list.completed_sources == 1

    with pytest.raises(ValueError):
        reading_list.change_status(source.id, "некорректный")


def test_reading_list_from_data() -> None:
    user = _make_user()
    source = _make_source()
    category = Category(1, "Наука")
    data = {
        "id": 1,
        "title": "Мой список",
        "owner": "ivan",
        "items": [
            {"source_id": 1, "category_id": 1, "status": "прочитан"},
        ],
        "status": "активен",
    }
    reading_list = ReadingList.from_data(
        data,
        {"ivan": user},
        {1: source},
        {1: category},
    )
    assert reading_list is not None
    assert reading_list.owner is user
    assert reading_list.items[0]["source"] is source
    assert reading_list.items[0]["category"] is category


def test_add_source_to_list_and_duplicate() -> None:
    user = _make_user()
    source = _make_source()
    category = Category(1, "Наука")
    reading_lists: dict[int, ReadingList] = {}
    reading_list = create_list(reading_lists, "Мой список", user)

    add_source_to_list(
        reading_lists, reading_list.id, source, category
    )
    assert reading_list.total_sources == 1

    with pytest.raises(ValueError):
        add_source_to_list(
            reading_lists, reading_list.id, source, category
        )


def test_change_status_via_function() -> None:
    user = _make_user()
    source = _make_source()
    reading_lists: dict[int, ReadingList] = {}
    reading_list = create_list(reading_lists, "Мой список", user)
    add_source_to_list(reading_lists, reading_list.id, source)

    change_reading_status(
        reading_lists, reading_list.id, source.id, "прочитан"
    )
    assert reading_list.items[0]["status"] == "прочитан"