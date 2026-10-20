from django.urls import path
from . import views

urlpatterns = [
    path("", views.sources_list, name="sources_list"),
    path("<int:source_id>/", views.source_detail, name="source_detail"),
]