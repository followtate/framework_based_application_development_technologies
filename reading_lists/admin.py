from django.contrib import admin

from .models import ReadingList, ReadingListItem


class ReadingListItemInline(admin.TabularInline):
    model = ReadingListItem
    extra = 0


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "owner__login")
    inlines = [ReadingListItemInline]


@admin.register(ReadingListItem)
class ReadingListItemAdmin(admin.ModelAdmin):
    list_display = ("reading_list", "source", "category", "status")
    list_filter = ("status",)