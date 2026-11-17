"""Представления для источников (Django ORM)."""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from categories.models import Category

from .models import Source

ALLOWED_SORT_FIELDS = {
    "title": "title",
    "author": "author",
    "year": "year",
    "type": "type",
}


def sources_list(request):
    """Список источников: поиск, фильтр, сортировка, пагинация."""
    sources = Source.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        sources = sources.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    source_type = request.GET.get("type", "").strip()
    if source_type in Source.SourceType.values:
        sources = sources.filter(type=source_type)

    year_from = request.GET.get("year_from", "").strip()
    if year_from.isdigit():
        sources = sources.filter(year__gte=int(year_from))

    sources = sources.exclude(year__lt=1900)

    sort_key = request.GET.get("sort", "title")
    order_field = ALLOWED_SORT_FIELDS.get(sort_key, "title")
    sources = sources.order_by(order_field)

    paginator = Paginator(sources, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "sources": page_obj.object_list,
        "query": query,
        "current_type": source_type,
        "current_sort": sort_key,
        "year_from": year_from,
        "types": Source.SourceType.choices,
    }
    return render(request, "sources/source_list.html", context)


def source_detail(request, source_id):
    """Карточка источника со списком категорий."""
    source = get_object_or_404(
        Source.objects.prefetch_related("categories"),
        id=source_id,
    )
    return render(
        request,
        "sources/source_detail.html",
        {"source": source},
    )


def source_search(request):
    """Отдельная страница поиска."""
    query = request.GET.get("q", "").strip()
    sources = Source.objects.none()
    if query:
        sources = Source.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).order_by("title")
    return render(
        request,
        "sources/search.html",
        {"sources": sources, "query": query},
    )


def stats(request):
    """Статистика: по типам и по категориям."""
    by_type = (
        Source.objects.values("type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    top_categories = (
        Category.objects.annotate(count=Count("sources"))
        .filter(count__gte=1)
        .order_by("-count", "name")
    )
    return render(
        request,
        "sources/stats.html",
        {"by_type": by_type, "top_categories": top_categories},
    )