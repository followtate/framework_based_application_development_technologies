"""Консольное приложение управления списками литературы."""

from categories import create_category, list_categories
from lists import (
    add_source_to_list,
    build_list_view,
    change_reading_status,
    create_list,
    list_reading_lists,
)
from sources import (
    add_source,
    filter_sources_by_type,
    find_sources,
    list_sources,
    sort_sources,
)
from storage import load_data, save_data
from users import list_users, register_user
from utils import input_int, input_str


def show_source_list(sources: list[dict]) -> None:
    """Вывести источники из списка."""
    if not sources:
        print("Источники не найдены.")
        return

    for source in sources:
        print(
            f"  [{source['id']}] {source['title']} — "
            f"{source['author']} ({source['year']}), {source['type']}"
        )


def show_sources(sources: dict[int, dict]) -> None:
    """Вывести все источники."""
    print("\nИсточники:")
    show_source_list(list_sources(sources))


def show_users(users: dict[str, dict]) -> None:
    """Вывести пользователей."""
    user_list = list_users(users)
    if not user_list:
        print("Пользователи отсутствуют.")
        return

    print("\nПользователи:")
    for user in user_list:
        print(f"  {user['login']}: {user['full_name']}, {user['email']}")


def show_categories(categories: dict[int, dict]) -> None:
    """Вывести категории."""
    category_list = list_categories(categories)
    if not category_list:
        print("Категории отсутствуют.")
        return

    print("\nКатегории:")
    for category in category_list:
        source_ids = ", ".join(
            str(source_id) for source_id in category["source_ids"]
        ) or "нет"
        print(
            f"  [{category['id']}] {category['name']} — "
            f"{category['description']}; источники: {source_ids}"
        )


def show_lists(reading_lists: dict[int, dict]) -> None:
    """Вывести списки литературы."""
    reading_list_values = list_reading_lists(reading_lists)
    if not reading_list_values:
        print("Списки отсутствуют.")
        return

    print("\nСписки литературы:")
    for reading_list in reading_list_values:
        print(
            f"  [{reading_list['id']}] {reading_list['title']} — "
            f"владелец: {reading_list['owner']}, "
            f"элементов: {len(reading_list['items'])}, "
            f"статус: {reading_list['status']}"
        )


def show_list_view(
    reading_lists: dict[int, dict],
    sources: dict[int, dict],
    categories: dict[int, dict],
    list_id: int,
) -> None:
    """Вывести содержимое списка."""
    rows = build_list_view(
        reading_lists, sources, categories, list_id
    )
    if not rows:
        print("Список пуст.")
        return

    print(f"\nСодержимое списка id={list_id}:")
    for row in rows:
        print(
            f"  [{row['source_id']}] {row['title']} — "
            f"{row['author']} ({row['year']}), {row['type']}, "
            f"категория: {row['category']}, статус: {row['status']}"
        )


def print_menu() -> None:
    """Вывести меню."""
    print("\n=== Сервис управления списками литературы ===")
    print("1. Зарегистрировать пользователя")
    print("2. Добавить источник")
    print("3. Создать категорию")
    print("4. Создать список литературы")
    print("5. Добавить источник в список")
    print("6. Изменить статус чтения")
    print("7. Показать источники")
    print("8. Найти источники")
    print("9. Отфильтровать источники по типу")
    print("10. Сортировать источники")
    print("11. Показать списки литературы")
    print("12. Показать содержимое списка")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    users, sources, categories, reading_lists = load_data()
    print("Данные загружены.")

    while True:
        print_menu()
        choice = input_int("Выберите действие: ", 0, 12)

        if choice == 0:
            print("Выход.")
            break

        try:
            if choice == 1:
                full_name = input_str("ФИО: ")
                email = input_str("Email: ")
                login = input_str("Логин: ")
                user = register_user(users, full_name, email, login)
                print(f"[OK] Пользователь зарегистрирован: {user['login']}")
            elif choice == 2:
                title = input_str("Название источника: ")
                author = input_str("Автор: ")
                year = input_int("Год издания: ", 0)
                source_type = input_str("Тип (книга/статья/ссылка): ")
                source = add_source(
                    sources, title, author, year, source_type
                )
                print(f"[OK] Источник добавлен: id={source['id']}")
            elif choice == 3:
                name = input_str("Название категории: ")
                description = input_str(
                    "Описание (можно пусто): ", allow_empty=True
                )
                category = create_category(
                    categories, name, description
                )
                print(f"[OK] Категория создана: id={category['id']}")
            elif choice == 4:
                show_users(users)
                owner = input_str("Логин владельца: ")
                if owner not in users:
                    raise ValueError("Пользователь не найден")
                title = input_str("Название списка: ")
                reading_list = create_list(
                    reading_lists, title, owner
                )
                print(f"[OK] Список создан: id={reading_list['id']}")
            elif choice == 5:
                show_lists(reading_lists)
                show_sources(sources)
                show_categories(categories)
                list_id = input_int("ID списка: ", 1)
                source_id = input_int("ID источника: ", 1)
                category_id = input_int(
                    "ID категории (0 — без категории): ", 0
                )
                add_source_to_list(
                    reading_lists,
                    sources,
                    categories,
                    list_id,
                    source_id,
                    None if category_id == 0 else category_id,
                )
                print("[OK] Источник добавлен в список.")
            elif choice == 6:
                show_lists(reading_lists)
                list_id = input_int("ID списка: ", 1)
                source_id = input_int("ID источника: ", 1)
                new_status = input_str(
                    "Новый статус (не начат/в процессе/прочитан): "
                )
                change_reading_status(
                    reading_lists, list_id, source_id, new_status
                )
                print("[OK] Статус изменён.")
            elif choice == 7:
                show_sources(sources)
            elif choice == 8:
                query = input_str("Поиск по названию или автору: ")
                show_source_list(find_sources(sources, query))
            elif choice == 9:
                source_type = input_str("Тип источника: ")
                found = list(
                    filter_sources_by_type(sources, source_type)
                )
                show_source_list(found)
            elif choice == 10:
                key = input_str("Сортировать по (title/author/year): ")
                reverse_raw = input_str("По убыванию? (д/н): ").lower()
                reverse = reverse_raw in {"д", "да", "y", "yes"}
                sorted_sources = sort_sources(sources, key, reverse)
                show_source_list(sorted_sources)
            elif choice == 11:
                show_lists(reading_lists)
            elif choice == 12:
                show_lists(reading_lists)
                list_id = input_int("ID списка: ", 1)
                show_list_view(
                    reading_lists, sources, categories, list_id
                )
        except (ValueError, KeyError) as exc:
            print(f"[ОШИБКА] {exc}")
        else:
            if choice in {1, 2, 3, 4, 5, 6}:
                save_data(users, sources, categories, reading_lists)
                print("[OK] Изменения сохранены в JSON.")


if __name__ == "__main__":
    main()
