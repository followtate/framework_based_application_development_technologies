"""Тесты категорий."""

import pytest

from models import Category, Source
from models.categories import create_category, get_category


def test_category_creation() -> None:
    category = Category(1, "Наука", "Научные источники")
    assert category.id == 1
    assert category.name == "Наука"
    assert category.source_count == 0


def test_category_add_source() -> None:
    category = Category(1, "Наука")
    source = Source(1, "Книга", "Автор", 2008, "книга")
    assert category.add_source(source)
    assert not category.add_source(source)
    assert category.source_count == 1


def test_category_from_data() -> None:
    sources = {
        1: Source(1, "Книга", "Автор", 2008, "книга"),
        2: Source(2, "Статья", "Автор", 2020, "статья"),
    }
    data = {
        "id": 1,
        "name": "Наука",
        "description": "Описание",
        "source_ids": [1, 2],
    }
    category = Category.from_data(data, sources)
    assert category.source_count == 2
    assert category.sources[0].id == 1


def test_category_str() -> None:
    category = Category(1, "Наука", "Описание")
    assert "Наука" in str(category)
    assert "Описание" in str(category)


def test_create_and_get_category() -> None:
    categories: dict[int, Category] = {}
    category = create_category(categories, "Наука")
    assert category.id == 1
    assert get_category(categories, 1) is category


def test_duplicate_category() -> None:
    categories: dict[int, Category] = {}
    create_category(categories, "Наука")
    with pytest.raises(ValueError):
        create_category(categories, "наука")