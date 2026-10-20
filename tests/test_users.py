"""Тесты пользователей."""

import pytest

from users import register_user


def test_register_user() -> None:
    users: dict[str, dict] = {}
    user = register_user(
        users, "Иван Иванов", "ivan@example.com", "ivan"
    )
    assert user["login"] == "ivan"
    assert "ivan" in users


def test_duplicate_login() -> None:
    users: dict[str, dict] = {}
    register_user(users, "Иван Иванов", "ivan@example.com", "ivan")
    with pytest.raises(ValueError):
        register_user(users, "Пётр Петров", "petr@example.com", "ivan")
