from django.urls import path
from . import views

app_name = "sources"

urlpatterns = [
    path("", views.sources_list, name="list"),
    path("<int:source_id>/", views.source_detail, name="detail"),
]