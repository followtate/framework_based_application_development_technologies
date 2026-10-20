from django.shortcuts import render
from django.http import HttpResponse

from homepage.views import page
from storage import load_categories, load_sources


def categories_list(request):
    sources = load_sources()
    categories = load_categories(sources)

    if not categories:
        content = """
        <h1 class="fw-bold mb-4">Категории</h1>
        <div class="text-center py-5 text-muted">
            <div class="display-4 mb-3"><i class="bi bi-tags"></i></div>
            <p class="lead">Категорий пока нет.</p>
        </div>
        """
        return HttpResponse(page(request, "Категории", content))

    cards = ""
    for cat in categories.values():
        cards += f"""
        <div class="col-md-6 col-lg-4">
            <div class="card card-hover shadow-sm border-0 h-100">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center mb-3">
                        <div class="stat-icon bg-warning-subtle text-warning me-3"
                             style="width: 44px; height: 44px; font-size: 1.2rem;">
                            <i class="bi bi-tag"></i>
                        </div>
                        <h5 class="fw-semibold mb-0">{cat.name}</h5>
                    </div>
                    <p class="text-muted small mb-3">
                        {cat.description or "Без описания"}
                    </p>
                    <span class="badge bg-primary-subtle text-primary">
                        {cat.source_count} источников
                    </span>
                </div>
            </div>
        </div>
        """

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="fw-bold mb-0">Категории</h1>
        <span class="badge bg-warning-subtle text-warning fs-6">
            Всего: {len(categories)}
        </span>
    </div>
    <div class="row g-3">{cards}</div>
    """
    return HttpResponse(page(request, "Категории", content))