"""Модели списков литературы и их элементов."""

from django.db import models

from categories.models import Category
from sources.models import Source
from users.models import User


class TimeStampedModel(models.Model):
    """Абстрактная модель с датой создания."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        abstract = True


class ReadingList(TimeStampedModel):
    """Список литературы пользователя."""

    class Status(models.TextChoices):
        ACTIVE = "активен", "Активен"
        ARCHIVED = "архив", "Архив"

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reading_lists",
        verbose_name="Владелец",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Список литературы"
        verbose_name_plural = "Списки литературы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.owner.login})"


class ReadingListItem(models.Model):
    """Элемент списка литературы — источник с категорией и статусом."""

    class ReadingStatus(models.TextChoices):
        NOT_STARTED = "не начат", "Не начат"
        IN_PROGRESS = "в процессе", "В процессе"
        DONE = "прочитан", "Прочитан"

    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Список",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="list_items",
        verbose_name="Источник",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="list_items",
        verbose_name="Категория",
    )
    status = models.CharField(
        max_length=20,
        choices=ReadingStatus.choices,
        default=ReadingStatus.NOT_STARTED,
        verbose_name="Статус чтения",
    )

    class Meta:
        verbose_name = "Элемент списка"
        verbose_name_plural = "Элементы списка"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.source.title} → {self.reading_list.title}"