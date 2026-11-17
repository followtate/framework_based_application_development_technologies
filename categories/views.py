"""Представления для категорий."""

from django.db.models import Count
from django.shortcuts import render

from .models import Category


def categories_list(request):
    """Список категорий с числом источников."""
    categories = Category.objects.annotate(
        source_count=Count("sources")
    ).order_by("name")
    return render(
        request,
        "categories/category_list.html",
        {"categories": categories},
    )