"""Тесты списков литературы."""

import pytest

from categories import create_category
from lists import (
    add_source_to_list,
    change_reading_status,
    create_list,
)
from sources import add_source


def test_add_source_to_list_and_duplicate() -> None:
    sources: dict[int, dict] = {}
    categories: dict[int, dict] = {}
    reading_lists: dict[int, dict] = {}

    source = add_source(
        sources, "Книга", "Автор", 2020, "книга"
    )
    category = create_category(categories, "Наука")
    reading_list = create_list(reading_lists, "Мой список", "ivan")

    add_source_to_list(
        reading_lists,
        sources,
        categories,
        reading_list["id"],
        source["id"],
        category["id"],
    )
    assert len(reading_list["items"]) == 1
    assert source["id"] in category["source_ids"]

    with pytest.raises(ValueError):
        add_source_to_list(
            reading_lists,
            sources,
            categories,
            reading_list["id"],
            source["id"],
            category["id"],
        )


def test_change_status() -> None:
    sources: dict[int, dict] = {}
    categories: dict[int, dict] = {}
    reading_lists: dict[int, dict] = {}

    source = add_source(
        sources, "Статья", "Автор", 2021, "статья"
    )
    reading_list = create_list(reading_lists, "Список", "ivan")

    add_source_to_list(
        reading_lists,
        sources,
        categories,
        reading_list["id"],
        source["id"],
    )
    change_reading_status(
        reading_lists, reading_list["id"], source["id"], "прочитан"
    )
    assert reading_list["items"][0]["status"] == "прочитан"
