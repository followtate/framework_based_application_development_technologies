"""Функции регистрации и поиска пользователей."""

from utils import now_iso


def register_user(
    users: dict[str, dict],
    full_name: str,
    email: str,
    login: str,
) -> dict:
    """Зарегистрировать пользователя и вернуть его карточку."""
    full_name = full_name.strip()
    email = email.strip().lower()
    login = login.strip()

    if not full_name:
        raise ValueError("ФИО пользователя не может быть пустым")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Некорректный email пользователя")
    if len(login) < 3:
        raise ValueError("Логин должен содержать минимум 3 символа")
    if login in users:
        raise ValueError("Пользователь с таким логином уже существует")

    user = {
        "full_name": full_name,
        "email": email,
        "login": login,
        "registered_at": now_iso(),
    }
    users[login] = user
    return user


def find_user(users: dict[str, dict], login: str) -> dict | None:
    """Найти пользователя по логину."""
    return users.get(login.strip())


def list_users(users: dict[str, dict]) -> list[dict]:
    """Вернуть список карточек пользователей."""
    return list(users.values())
