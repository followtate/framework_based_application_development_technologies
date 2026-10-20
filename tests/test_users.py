"""Тесты пользователей."""

import pytest

from models import User
from models.users import find_user, register_user


def test_user_creation() -> None:
    user = User(1, "Иван Петров", "ivan@example.com", "ivan")
    assert user.id == 1
    assert user.full_name == "Иван Петров"
    assert user.email == "ivan@example.com"
    assert user.login == "ivan"


def test_user_str() -> None:
    user = User(1, "Иван Петров", "ivan@example.com", "ivan")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data() -> None:
    data = {
        "id": 5,
        "full_name": "Анна Смирнова",
        "email": "anna@example.com",
        "login": "anna",
    }
    user = User.from_data(data)
    assert user.id == 5
    assert user.login == "anna"
    assert user.display_name == "Анна Смирнова"


def test_validate_email() -> None:
    assert User.validate_email("a@b.c")
    assert not User.validate_email("invalid")


def test_register_and_find() -> None:
    users: dict[str, User] = {}
    user = register_user(users, "Пётр", "petr@example.com", "petr")
    assert user.id == 1
    assert find_user(users, "petr") is user


def test_duplicate_login() -> None:
    users: dict[str, User] = {}
    register_user(users, "Пётр", "petr@example.com", "petr")
    with pytest.raises(ValueError):
        register_user(users, "Иван", "ivan@example.com", "petr")