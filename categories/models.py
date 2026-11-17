"""Модель тематической категории."""

from django.db import models

from sources.models import Source


class Category(models.Model):
    """Тематическая категория источников."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    sources = models.ManyToManyField(
        Source,
        related_name="categories",
        blank=True,
        verbose_name="Источники",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name