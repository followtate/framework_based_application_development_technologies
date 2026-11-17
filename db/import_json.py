"""Импорт данных проекта из JSON-файлов в SQLite."""

import json

from db.database import get_connection

USERS_FILE = "data/users.json"
SOURCES_FILE = "data/sources.json"
CATEGORIES_FILE = "data/categories.json"
LISTS_FILE = "data/reading_lists.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn):
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, login, full_name, email, registered_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                user["id"],
                user["login"],
                user["full_name"],
                user["email"],
                user.get("registered_at"),
            )
            for user in users.values()
        ],
    )


def import_sources(conn):
    sources = load_json(SOURCES_FILE)
    conn.executemany(
        """
        INSERT INTO sources (id, title, author, year, type)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                source["id"],
                source["title"],
                source["author"],
                int(source["year"]),
                source["type"],
            )
            for source in sources.values()
        ],
    )


def import_categories(conn):
    categories = load_json(CATEGORIES_FILE)
    rows = []
    links = []
    for category in categories.values():
        rows.append(
            (
                category["id"],
                category["name"],
                category.get("description", ""),
            )
        )
        for source_id in category.get("source_ids", []):
            links.append((category["id"], int(source_id)))

    conn.executemany(
        "INSERT INTO categories (id, name, description) VALUES (?, ?, ?)",
        rows,
    )
    conn.executemany(
        "INSERT INTO category_sources (category_id, source_id) VALUES (?, ?)",
        links,
    )


def import_reading_lists(conn):
    lists = load_json(LISTS_FILE)
    users = load_json(USERS_FILE)
    login_to_id = {u["login"]: u["id"] for u in users.values()}

    list_rows = []
    item_rows = []
    item_id = 1
    for reading_list in lists.values():
        list_rows.append(
            (
                reading_list["id"],
                reading_list["title"],
                login_to_id[reading_list["owner"]],
                reading_list.get("status", "активен"),
                reading_list.get("created_at"),
            )
        )
        for item in reading_list.get("items", []):
            item_rows.append(
                (
                    item_id,
                    reading_list["id"],
                    int(item["source_id"]),
                    item.get("category_id"),
                    item.get("status", "не начат"),
                )
            )
            item_id += 1

    conn.executemany(
        """
        INSERT INTO reading_lists (id, title, owner_id, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        list_rows,
    )
    conn.executemany(
        """
        INSERT INTO reading_list_items
        (id, reading_list_id, source_id, category_id, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        item_rows,
    )


def main():
    conn = get_connection()
    try:
        import_users(conn)
        import_sources(conn)
        import_categories(conn)
        import_reading_lists(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("Импорт завершён.")


if __name__ == "__main__":
    main()