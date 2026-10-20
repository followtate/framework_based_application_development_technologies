from django.shortcuts import render
from django.http import HttpResponse

from homepage.views import page
from models.lists import get_list
from storage import load_data


def lists(request):
    _, _, _, reading_lists = load_data()

    if not reading_lists:
        content = """
        <h1 class="fw-bold mb-4">Списки литературы</h1>
        <div class="text-center py-5 text-muted">
            <div class="display-4 mb-3"><i class="bi bi-bookmarks"></i></div>
            <p class="lead">Списков пока нет.</p>
        </div>
        """
        return HttpResponse(page(request, "Списки литературы", content))

    cards = ""
    for rl in reading_lists.values():
        percent = 0
        if rl.total_sources > 0:
            percent = int(rl.completed_sources / rl.total_sources * 100)
        cards += f"""
        <div class="col-md-6">
            <div class="card card-hover shadow-sm border-0 h-100">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="fw-semibold mb-0">{rl.title}</h5>
                        <span class="badge bg-success-subtle text-success">
                            {rl.total_sources} источников
                        </span>
                    </div>
                    <p class="text-muted small mb-3">
                        <i class="bi bi-person me-1"></i>{rl.owner.display_name}
                    </p>
                    <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: {percent}%;"></div>
                    </div>
                    <small class="text-muted">
                        Прочитано: {rl.completed_sources} из {rl.total_sources}
                    </small>
                </div>
                <div class="card-footer bg-transparent border-0 pt-0 px-4 pb-3">
                    <a href="/lists/{rl.id}/" class="btn btn-sm btn-outline-primary">
                        Открыть <i class="bi bi-arrow-right ms-1"></i>
                    </a>
                </div>
            </div>
        </div>
        """

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="fw-bold mb-0">Списки литературы</h1>
        <span class="badge bg-success-subtle text-success fs-6">
            Всего: {len(reading_lists)}
        </span>
    </div>
    <div class="row g-3">{cards}</div>
    """
    return HttpResponse(page(request, "Списки литературы", content))


def list_detail(request, list_id):
    _, _, _, reading_lists = load_data()

    try:
        rl = get_list(reading_lists, list_id)
    except KeyError:
        content = """
        <div class="text-center py-5">
            <div class="display-4 text-warning mb-3">
                <i class="bi bi-file-earmark-x"></i>
            </div>
            <h1 class="fw-bold mb-3">Список не найден</h1>
            <a href="/lists/" class="btn btn-outline-secondary mt-3">
                <i class="bi bi-arrow-left me-1"></i> К спискам
            </a>
        </div>
        """
        return HttpResponse(
            page(request, "Список не найден", content), status=404
        )

    percent = 0
    if rl.total_sources > 0:
        percent = int(rl.completed_sources / rl.total_sources * 100)

    if rl.items:
        items_html = ""
        for item in rl.items:
            source = item["source"]
            category = item["category"]
            cat_name = category.name if category else "без категории"

            if item["status"] == "прочитан":
                status_class = "success"
            elif item["status"] == "в процессе":
                status_class = "warning"
            else:
                status_class = "secondary"

            items_html += f"""
            <div class="list-group-item d-flex justify-content-between align-items-center py-3">
                <div>
                    <a href="/sources/{source.id}/"
                       class="text-decoration-none fw-semibold">
                        {source.title}
                    </a>
                    <div class="text-muted small mt-1">
                        <i class="bi bi-person me-1"></i>{source.author}
                        <span class="mx-2">·</span>
                        {source.year}
                        <span class="mx-2">·</span>
                        <i class="bi bi-tag me-1"></i>{cat_name}
                    </div>
                </div>
                <span class="badge bg-{status_class}-subtle text-{status_class}">
                    {item["status"]}
                </span>
            </div>
            """
    else:
        items_html = """
        <div class="text-center py-5 text-muted">
            <div class="display-6 mb-3"><i class="bi bi-inbox"></i></div>
            <p>В этом списке пока нет источников.</p>
        </div>
        """

    content = f"""
    <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Главная</a></li>
            <li class="breadcrumb-item"><a href="/lists/">Списки</a></li>
            <li class="breadcrumb-item active">{rl.title}</li>
        </ol>
    </nav>
    <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-4">
            <h1 class="fw-bold mb-2">{rl.title}</h1>
            <p class="text-muted mb-3">
                <i class="bi bi-person me-1"></i>{rl.owner.display_name}
                <small>({rl.owner.login})</small>
            </p>
            <div class="d-flex justify-content-between mb-2">
                <small class="text-muted">Прогресс чтения</small>
                <small class="fw-semibold">
                    {rl.completed_sources} / {rl.total_sources}
                </small>
            </div>
            <div class="progress" style="height: 8px;">
                <div class="progress-bar bg-success" style="width: {percent}%;"></div>
            </div>
        </div>
    </div>
    <div class="card shadow-sm border-0">
        <div class="list-group list-group-flush">{items_html}</div>
    </div>
    <div class="mt-4">
        <a href="/lists/" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left me-1"></i> К спискам
        </a>
    </div>
    """
    return HttpResponse(page(request, rl.title, content))