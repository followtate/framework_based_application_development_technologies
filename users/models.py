"""Модель пользователя-владельца списков литературы."""

from django.db import models


class User(models.Model):
    """Пользователь системы — владелец списков литературы."""

    login = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Логин",
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name="ФИО",
    )
    email = models.EmailField(
        verbose_name="Email",
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["login"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.login})"