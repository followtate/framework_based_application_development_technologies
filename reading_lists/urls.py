from django.urls import path
from . import views

urlpatterns = [
    path("", views.lists, name="lists"),
    path("<int:list_id>/", views.list_detail, name="list_detail"),
]