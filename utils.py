"""Вспомогательные функции ввода и идентификаторов."""

from datetime import date, datetime


def input_str(prompt: str, allow_empty: bool = False) -> str:
    """Запросить строку; при необходимости запретить пустой ввод."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Поле не может быть пустым. Повторите ввод.")


def input_int(
    prompt: str,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    """Запросить целое число с проверкой границ."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Значение должно быть не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Значение должно быть не больше {max_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ.")


def next_id(items: dict[int, dict]) -> int:
    """Вернуть следующий свободный целочисленный идентификатор."""
    return max(items, default=0) + 1


def now_iso() -> str:
    """Вернуть текущие дату и время в формате ISO."""
    return datetime.now().isoformat(timespec="seconds")
