from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("login", "full_name", "email", "registered_at")
    search_fields = ("login", "full_name", "email")