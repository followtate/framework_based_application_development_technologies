"""Модель источника (книга, статья, ссылка)."""

from django.db import models


class Source(models.Model):
    """Источник — книга, статья или ссылка."""

    class SourceType(models.TextChoices):
        BOOK = "книга", "Книга"
        ARTICLE = "статья", "Статья"
        LINK = "ссылка", "Ссылка"

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    author = models.CharField(
        max_length=150,
        verbose_name="Автор",
    )
    year = models.PositiveIntegerField(
        verbose_name="Год издания",
    )
    type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        verbose_name="Тип",
    )

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} — {self.author} ({self.year})"