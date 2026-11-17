from django.urls import path

from . import views

app_name = "sources"

urlpatterns = [
    path("", views.sources_list, name="list"),
    path("search/", views.source_search, name="search"),
    path("stats/", views.stats, name="stats"),
    path("<int:source_id>/", views.source_detail, name="detail"),
]