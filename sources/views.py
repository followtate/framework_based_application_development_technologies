from django.shortcuts import render
from django.http import HttpResponse

from homepage.views import page
from models.sources import get_source
from storage import load_sources


def sources_list(request):
    sources = load_sources()

    if not sources:
        content = """
        <h1 class="fw-bold mb-4">Источники</h1>
        <div class="text-center py-5 text-muted">
            <div class="display-4 mb-3"><i class="bi bi-inbox"></i></div>
            <p class="lead">Источников пока нет.</p>
        </div>
        """
        return HttpResponse(page(request, "Источники", content))

    cards = ""
    for src in sources.values():
        type_class = "primary"
        if src.type == "статья":
            type_class = "info"
        elif src.type == "ссылка":
            type_class = "warning"

        cards += f"""
        <div class="col-md-6 col-lg-4">
            <div class="card card-hover shadow-sm border-0 h-100">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-{type_class}-subtle text-{type_class}">
                            {src.type}
                        </span>
                        <small class="text-muted">{src.year}</small>
                    </div>
                    <h5 class="card-title fw-semibold mb-2">{src.title}</h5>
                    <p class="text-muted mb-0">
                        <i class="bi bi-person me-1"></i>{src.author}
                    </p>
                </div>
                <div class="card-footer bg-transparent border-0 pt-0 px-4 pb-3">
                    <a href="/sources/{src.id}/" class="btn btn-sm btn-outline-primary">
                        Подробнее <i class="bi bi-arrow-right ms-1"></i>
                    </a>
                </div>
            </div>
        </div>
        """

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="fw-bold mb-0">Источники</h1>
        <span class="badge bg-primary-subtle text-primary fs-6">
            Всего: {len(sources)}
        </span>
    </div>
    <div class="row g-3">{cards}</div>
    """
    return HttpResponse(page(request, "Источники", content))


def source_detail(request, source_id):
    sources = load_sources()
    try:
        source = get_source(sources, source_id)
    except KeyError:
        content = """
        <div class="text-center py-5">
            <div class="display-4 text-warning mb-3">
                <i class="bi bi-file-earmark-x"></i>
            </div>
            <h1 class="fw-bold mb-3">Источник не найден</h1>
            <p class="text-muted mb-4">Возможно, id указан неверно.</p>
            <a href="/sources/" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-1"></i> К источникам
            </a>
        </div>
        """
        return HttpResponse(
            page(request, "Источник не найден", content), status=404
        )

    content = f"""
    <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Главная</a></li>
            <li class="breadcrumb-item"><a href="/sources/">Источники</a></li>
            <li class="breadcrumb-item active">{source.title}</li>
        </ol>
    </nav>
    <div class="card shadow-sm border-0">
        <div class="card-body p-4 p-md-5">
            <div class="d-flex justify-content-between align-items-start mb-4 flex-wrap gap-3">
                <div>
                    <h1 class="fw-bold mb-2">{source.title}</h1>
                    <p class="text-muted fs-5 mb-0">
                        <i class="bi bi-person me-1"></i>{source.author}
                        <span class="mx-2">·</span>
                        <i class="bi bi-calendar me-1"></i>{source.year}
                    </p>
                </div>
                <span class="badge bg-primary-subtle text-primary fs-6">
                    {source.type}
                </span>
            </div>
            <hr class="my-4">
            <div class="row g-3">
                <div class="col-sm-4">
                    <small class="text-muted d-block">ID</small>
                    <strong>#{source.id}</strong>
                </div>
                <div class="col-sm-4">
                    <small class="text-muted d-block">Тип</small>
                    <strong>{source.type}</strong>
                </div>
                <div class="col-sm-4">
                    <small class="text-muted d-block">Год</small>
                    <strong>{source.year}</strong>
                </div>
            </div>
            <div class="mt-4">
                <a href="/sources/" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left me-1"></i> К источникам
                </a>
            </div>
        </div>
    </div>
    """
    return HttpResponse(page(request, source.title, content))