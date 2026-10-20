from django.contrib import admin
from django.urls import include, path

# Обработчик ошибки 404
handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("sources/", include("sources.urls")),
    path("lists/", include("reading_lists.urls")),
    path("categories/", include("categories.urls")),
]