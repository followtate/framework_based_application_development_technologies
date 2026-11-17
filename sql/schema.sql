CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    registered_at TEXT
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS category_sources (
    category_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    PRIMARY KEY (category_id, source_id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS reading_lists (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'активен',
    created_at TEXT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reading_list_items (
    id INTEGER PRIMARY KEY,
    reading_list_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    category_id INTEGER,
    status TEXT NOT NULL DEFAULT 'не начат',
    FOREIGN KEY (reading_list_id) REFERENCES reading_lists(id),
    FOREIGN KEY (source_id) REFERENCES sources(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);