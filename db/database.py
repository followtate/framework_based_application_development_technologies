"""Подключение к SQLite для проекта «Читальня»."""

import sqlite3

DB_PATH = "data/literature.sqlite"


def get_connection():
    """Открыть соединение с включённой проверкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn