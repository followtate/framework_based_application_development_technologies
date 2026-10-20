"""Класс User и функции работы с пользователями."""

from __future__ import annotations

from datetime import datetime


class User:
    """Пользователь системы — владелец списков литературы."""

    def __init__(
        self,
        user_id: int,
        full_name: str,
        email: str,
        login: str,
        registered_at: str = "",
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.full_name = full_name
        self.email = email
        self.login = login
        self.registered_at = (
            registered_at or datetime.now().isoformat(timespec="seconds")
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверить корректность email."""
        email = email.strip()
        return "@" in email and "." in email.split("@")[-1]

    @property
    def display_name(self) -> str:
        """Отображаемое имя пользователя."""
        return self.full_name.strip() or self.login

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Восстановить пользователя из данных JSON."""
        return cls(
            user_id=int(data["id"]),
            full_name=data["full_name"],
            email=data["email"],
            login=data["login"],
            registered_at=data.get("registered_at", ""),
        )

    def to_dict(self) -> dict:
        """Преобразовать пользователя в структуру для JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "login": self.login,
            "registered_at": self.registered_at,
        }

    def __str__(self) -> str:
        return f"{self.display_name} ({self.login}, {self.email})"


def next_user_id(users: dict[str, "User"]) -> int:
    """Следующий свободный идентификатор пользователя."""
    return max((user.id for user in users.values()), default=0) + 1


def register_user(
    users: dict[str, "User"],
    full_name: str,
    email: str,
    login: str,
) -> "User":
    """Зарегистрировать пользователя и добавить его в коллекцию."""
    full_name = full_name.strip()
    email = email.strip().lower()
    login = login.strip()

    if not full_name:
        raise ValueError("ФИО пользователя не может быть пустым")
    if not User.validate_email(email):
        raise ValueError("Некорректный email пользователя")
    if len(login) < 3:
        raise ValueError("Логин должен содержать минимум 3 символа")
    if login in users:
        raise ValueError("Пользователь с таким логином уже существует")

    user = User(
        user_id=next_user_id(users),
        full_name=full_name,
        email=email,
        login=login,
    )
    users[login] = user
    return user


def find_user(users: dict[str, "User"], login: str) -> "User | None":
    """Найти пользователя по логину."""
    return users.get(login.strip())


def find_user_by_id(users: dict[str, "User"], user_id: int) -> "User | None":
    """Найти пользователя по идентификатору."""
    for user in users.values():
        if user.id == user_id:
            return user
    return None


def list_users(users: dict[str, "User"]) -> list["User"]:
    """Вернуть список пользователей."""
    return list(users.values())