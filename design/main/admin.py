from django.contrib import admin
from .models import Claim, Category

@admin.register(Claim)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_time', 'user']
    list_filter = ['status', 'created_time']
    search_fields = ['name', 'description', 'user__username']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']