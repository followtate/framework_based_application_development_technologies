from django.http import HttpResponse

from storage import load_data

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>__TITLE__ — Читальня</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: #f8f9fb;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        main { flex: 1; }
        .brand-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-right: 10px;
        }
        .nav-link {
            font-weight: 500;
            border-radius: 8px;
            padding: 0.5rem 1rem !important;
        }
        .nav-link.active { background: rgba(255,255,255,0.12); }
        .card-hover {
            transition: transform .15s ease, box-shadow .15s ease;
        }
        .card-hover:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 2.5rem;
            border-radius: 1rem;
        }
        .stat-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            border-radius: 14px;
            font-size: 1.75rem;
        }
        footer {
            background: white;
            border-top: 1px solid #e9ecef;
            padding: 1.5rem 0;
            color: #6c757d;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #1e293b, #0f172a);">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="/">
                <span class="brand-icon"><i class="bi bi-book"></i></span>
                <strong>Читальня</strong>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link __ACTIVE_SOURCES__" href="/sources/">
                            <i class="bi bi-collection"></i> Источники
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link __ACTIVE_LISTS__" href="/lists/">
                            <i class="bi bi-bookmarks"></i> Списки
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link __ACTIVE_CATEGORIES__" href="/categories/">
                            <i class="bi bi-tags"></i> Категории
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <main class="container py-4">
        __CONTENT__
    </main>
    <footer>
        <div class="container text-center">
            &copy; 2026 <strong>Читальня</strong> — сервис управления списками литературы
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""


def page(request, title: str, content: str) -> str:
    """Единый HTML-каркас с навбаром, стилями и футером."""
    path = request.path
    html = PAGE_TEMPLATE
    html = html.replace("__TITLE__", title)
    html = html.replace("__CONTENT__", content)
    html = html.replace(
        "__ACTIVE_SOURCES__",
        "active" if path.startswith("/sources") else "",
    )
    html = html.replace(
        "__ACTIVE_LISTS__",
        "active" if path.startswith("/lists") else "",
    )
    html = html.replace(
        "__ACTIVE_CATEGORIES__",
        "active" if path.startswith("/categories") else "",
    )
    return html


def index(request):
    """Главная страница со статистикой и навигацией."""
    _, sources, categories, reading_lists = load_data()
    content = f"""
    <div class="hero shadow mb-5">
        <h1 class="display-4 fw-bold mb-3">Читальня</h1>
        <p class="lead mb-4" style="max-width: 640px;">
            Управляйте библиографией, распределяйте источники по категориям
            и ведите списки чтения — всё в одном месте.
        </p>
        <a href="/sources/" class="btn btn-light btn-lg px-4">
            Начать <i class="bi bi-arrow-right ms-1"></i>
        </a>
    </div>

    <div class="row g-4">
        <div class="col-md-4">
            <div class="card card-hover shadow-sm border-0 h-100 position-relative">
                <div class="card-body text-center p-4">
                    <div class="stat-icon bg-primary-subtle text-primary mx-auto">
                        <i class="bi bi-collection"></i>
                    </div>
                    <h2 class="fw-bold mt-3 mb-1">{len(sources)}</h2>
                    <p class="text-muted mb-0">Источников</p>
                    <a href="/sources/" class="stretched-link"></a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card card-hover shadow-sm border-0 h-100 position-relative">
                <div class="card-body text-center p-4">
                    <div class="stat-icon bg-success-subtle text-success mx-auto">
                        <i class="bi bi-bookmarks"></i>
                    </div>
                    <h2 class="fw-bold mt-3 mb-1">{len(reading_lists)}</h2>
                    <p class="text-muted mb-0">Списков чтения</p>
                    <a href="/lists/" class="stretched-link"></a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card card-hover shadow-sm border-0 h-100 position-relative">
                <div class="card-body text-center p-4">
                    <div class="stat-icon bg-warning-subtle text-warning mx-auto">
                        <i class="bi bi-tags"></i>
                    </div>
                    <h2 class="fw-bold mt-3 mb-1">{len(categories)}</h2>
                    <p class="text-muted mb-0">Категорий</p>
                    <a href="/categories/" class="stretched-link"></a>
                </div>
            </div>
        </div>
    </div>
    """
    return HttpResponse(page(request, "Главная", content))


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <div class="text-center py-5">
        <div class="display-1 text-danger mb-3">
            <i class="bi bi-exclamation-triangle"></i>
        </div>
        <h1 class="display-5 fw-bold mb-3">404</h1>
        <p class="lead text-muted mb-4">Такой страницы не существует.</p>
        <a href="/" class="btn btn-primary px-4">
            <i class="bi bi-house me-1"></i> На главную
        </a>
    </div>
    """
    return HttpResponse(
        page(request, "404 — Страница не найдена", content),
        status=404,
    )