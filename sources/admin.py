from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "type")
    list_filter = ("type",)
    search_fields = ("title", "author")