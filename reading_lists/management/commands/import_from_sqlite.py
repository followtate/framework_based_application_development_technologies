"""Перенос данных из SQLite-БД ПР7 в Django ORM."""

import sqlite3
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from categories.models import Category
from reading_lists.models import ReadingList, ReadingListItem
from sources.models import Source
from users.models import User

DB_PATH = Path("data/literature.sqlite")


class Command(BaseCommand):
    help = "Переносит данные из data/literature.sqlite в Django ORM"

    def handle(self, *args, **options):
        if not DB_PATH.exists():
            self.stderr.write(f"Файл {DB_PATH} не найден")
            return

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        with transaction.atomic():
            self._import_users(conn)
            self._import_sources(conn)
            self._import_categories(conn)
            self._import_reading_lists(conn)

        conn.close()
        self.stdout.write(self.style.SUCCESS("Импорт завершён"))

    def _import_users(self, conn):
        for row in conn.execute("SELECT * FROM users"):
            User.objects.update_or_create(
                login=row["login"],
                defaults={
                    "full_name": row["full_name"],
                    "email": row["email"],
                },
            )

    def _import_sources(self, conn):
        for row in conn.execute("SELECT * FROM sources"):
            Source.objects.update_or_create(
                id=row["id"],
                defaults={
                    "title": row["title"],
                    "author": row["author"],
                    "year": row["year"],
                    "type": row["type"],
                },
            )

    def _import_categories(self, conn):
        for row in conn.execute("SELECT * FROM categories"):
            category, _ = Category.objects.update_or_create(
                id=row["id"],
                defaults={
                    "name": row["name"],
                    "description": row["description"] or "",
                },
            )
            source_ids = [
                r["source_id"]
                for r in conn.execute(
                    "SELECT source_id FROM category_sources "
                    "WHERE category_id = ?",
                    (row["id"],),
                )
            ]
            category.sources.set(
                Source.objects.filter(id__in=source_ids)
            )

    def _import_reading_lists(self, conn):
        for row in conn.execute("SELECT * FROM reading_lists"):
            owner = User.objects.filter(id=row["owner_id"]).first()
            if owner is None:
                owner = User.objects.filter(login="ivan").first()
            if owner is None:
                self.stderr.write(
                    f"Пользователь для списка {row['id']} не найден"
                )
                continue
            rl, _ = ReadingList.objects.update_or_create(
                id=row["id"],
                defaults={
                    "title": row["title"],
                    "owner": owner,
                    "status": row["status"],
                },
            )
            for item in conn.execute(
                "SELECT * FROM reading_list_items "
                "WHERE reading_list_id = ?",
                (row["id"],),
            ):
                category = None
                if item["category_id"]:
                    category = Category.objects.filter(
                        id=item["category_id"]
                    ).first()
                source = Source.objects.filter(
                    id=item["source_id"]
                ).first()
                if source is None:
                    continue
                ReadingListItem.objects.update_or_create(
                    reading_list=rl,
                    source=source,
                    defaults={
                        "category": category,
                        "status": item["status"],
                    },
                )