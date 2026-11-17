"""Представления для списков литературы."""

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import ReadingList, ReadingListItem


def lists(request):
    """Список списков литературы с подсчётом элементов."""
    reading_lists = (
        ReadingList.objects.select_related("owner")
        .annotate(
            total_sources=Count("items"),
            completed_sources=Count(
                "items",
                filter=Q(items__status=ReadingListItem.ReadingStatus.DONE),
            ),
        )
        .order_by("-created_at")
    )
    return render(
        request,
        "reading_lists/list_list.html",
        {"lists": reading_lists},
    )


def list_detail(request, list_id):
    """Содержимое списка литературы."""
    reading_list = get_object_or_404(
        ReadingList.objects.select_related("owner"),
        id=list_id,
    )
    items = reading_list.items.select_related("source", "category")
    return render(
        request,
        "reading_lists/list_detail.html",
        {"reading_list": reading_list, "items": items},
    )