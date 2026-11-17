"""Главная страница и обработка 404."""

from django.db.models import Count
from django.shortcuts import render

from categories.models import Category
from reading_lists.models import ReadingList
from sources.models import Source


def index(request):
    """Главная со сводной статистикой."""
    stats = {
        "sources_count": Source.objects.aggregate(
            total=Count("id")
        )["total"],
        "categories_count": Category.objects.aggregate(
            total=Count("id")
        )["total"],
        "lists_count": ReadingList.objects.aggregate(
            total=Count("id")
        )["total"],
        "by_type": Source.objects.values("type")
        .annotate(count=Count("id"))
        .order_by("-count"),
    }
    return render(request, "homepage/index.html", {"stats": stats})


def page_not_found(request, exception):
    return render(request, "404.html", status=404)