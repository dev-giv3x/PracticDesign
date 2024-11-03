from django.contrib import admin
from .models import Claim, Category
from django.utils.html import format_html
from .forms import ClaimStatusForm


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    form = ClaimStatusForm
    list_display = ['name', 'status', 'created_time', 'user',]
    list_filter = ['status', 'created_time']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['name', 'description', 'category', 'created_time', 'user', 'photo','display_photo', 'display_admin_photo']
    fields = ['name', 'description', 'category', 'comment','status', 'created_time', 'user', 'photo', 'admin_photo','display_photo', 'display_admin_photo']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'completed':
            return super().get_readonly_fields(request, obj) + ['comment', 'admin_photo', 'status']
        return super().get_readonly_fields(request, obj)

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height: auto;"/>', obj.photo.url)
        return "Нет изображения"

    display_photo.short_description = 'user photo'

    def display_admin_photo(self, obj):
        if obj.admin_photo:
            return format_html('<img src="{}" style="width: 100px; height: auto;"/>', obj.admin_photo.url)
        return "Нет изображения"

    display_admin_photo.short_description = 'admin photo'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']