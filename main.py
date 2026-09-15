
from datetime import date, datetime


def register_user(full_name: str, email: str, login: str) -> dict:
    """Регистрирует пользователя и возвращает его карточку."""
    if not full_name.strip():
        raise ValueError("ФИО пользователя не может быть пустым")
    if "@" not in email or "." not in email:
        raise ValueError("Некорректный email пользователя")
    if len(login.strip()) < 3:
        raise ValueError("Логин должен содержать минимум 3 символа")

    user = {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "login": login.strip(),
        "registered_at": datetime.now(),
    }
    print(f"[OK] Пользователь зарегистрирован: {user['full_name']} "
          f"(логин: {user['login']}, email: {user['email']})")
    return user

 
def add_source(title: str, author: str, year: int, source_type: str) -> dict:
    """Добавляет источник (книга, статья, ссылка) и возвращает его карточку."""
    allowed_types = {"книга", "статья", "ссылка"}
    if not title.strip():
        raise ValueError("Название источника не может быть пустым")
    if year < 0 or year > date.today().year + 1:
        raise ValueError("Некорректный год издания")
    if source_type not in allowed_types:
        raise ValueError(f"Недопустимый тип источника. "
                         f"Разрешены: {', '.join(allowed_types)}")

    source = {
        "title": title.strip(),
        "author": author.strip(),
        "year": int(year),
        "type": source_type,
    }
    print(f"[OK] Источник добавлен: «{source['title']}», "
          f"{source['author']} ({source['year']}), тип: {source['type']}")
    return source


def create_category(name: str, description: str = "") -> dict:
    """Создаёт категорию для группировки источников."""
    if not name.strip():
        raise ValueError("Название категории не может быть пустым")

    category = {
        "name": name.strip(),
        "description": description.strip(),
        "sources": [],
    }
    print(f"[OK] Категория создана: «{category['name']}»")
    return category


def create_list(title: str, owner: dict) -> dict:
    """Создаёт пользовательский список литературы."""
    if not title.strip():
        raise ValueError("Название списка не может быть пустым")
    if "login" not in owner:
        raise ValueError("Некорректный владелец списка")

    reading_list = {
        "title": title.strip(),
        "owner": owner["login"],
        "created_at": datetime.now(),
        "items": [],
        "status": "активен",
    }
    print(f"[OK] Список создан: «{reading_list['title']}» "
          f"для пользователя {reading_list['owner']}")
    return reading_list


def add_source_to_list(reading_list: dict, source: dict,
                       category: dict | None = None) -> dict:
    """Добавляет источник в список с проверкой дублирования."""
    if not reading_list.get("items"):
        reading_list["items"] = []

    # Проверка дублирования
    for item in reading_list["items"]:
        if (item["title"].lower() == source["title"].lower()
                and item["author"].lower() == source["author"].lower()):
            print(f"[ОТКАЗ] Источник «{source['title']}» уже есть в списке "
                  f"«{reading_list['title']}»")
            return reading_list

    entry = {
        "title": source["title"],
        "author": source["author"],
        "year": source["year"],
        "type": source["type"],
        "category": category["name"] if category else "без категории",
        "status": "не начат",
    }
    reading_list["items"].append(entry)

    if category is not None and "sources" in category:
        category["sources"].append(source["title"])

    print(f"[OK] Источник «{entry['title']}» добавлен в список "
          f"«{reading_list['title']}» (категория: {entry['category']}, "
          f"статус: {entry['status']})")
    return reading_list


def change_reading_status(reading_list: dict, source_title: str,
                          new_status: str) -> dict:
    """Меняет статус чтения источника внутри списка."""
    allowed = {"не начат", "в процессе", "прочитан"}
    if new_status not in allowed:
        raise ValueError(f"Недопустимый статус: {new_status}. "
                         f"Разрешены: {', '.join(allowed)}")

    for item in reading_list.get("items", []):
        if item["title"].lower() == source_title.lower():
            old = item["status"]
            item["status"] = new_status
            print(f"[OK] Статус «{item['title']}» изменён: "
                  f"«{old}» → «{new_status}»")
            return reading_list

    print(f"[ОТКАЗ] Источник «{source_title}» не найден в списке")
    return reading_list



def main() -> None:
    user = register_user(
        full_name="user ",
        email="eee@Example.com",
        login="eee",
    )
    category = create_category(
        name="Программирование",
        description="Книги и статьи по разработке ПО",
    )
    source_book = add_source(
        title="Чистый код",
        author="Роберт Мартин",
        year=2008,
        source_type="книга",
    )
    source_article = add_source(
        title="PEP 8 — Style Guide for Python Code",
        author="Guido van Rossum",
        year=2001,
        source_type="статья",
    )
    reading_list = create_list(
        title="Чтение на семестр",
        owner=user,
    )
    add_source_to_list(reading_list, source_book, category)
    add_source_to_list(reading_list, source_article, category)

    add_source_to_list(reading_list, source_book, category)

    print(f"Список «{reading_list['title']}» пользователя "
          f"{reading_list['owner']} содержит "
          f"{len(reading_list['items'])} источник(ов):")
    for i, item in enumerate(reading_list["items"], start=1):
        print(f"  {i}. {item['title']} — {item['author']} "
              f"({item['year']}), категория: {item['category']}, "
              f"статус: {item['status']}")
    


if __name__ == "__main__":
    main()