from django.shortcuts import render

from storage import load_categories, load_sources


def categories_list(request):
    sources = load_sources()
    categories = load_categories(sources)
    context = {"categories": list(categories.values())}
    return render(request, "categories/category_list.html", context)