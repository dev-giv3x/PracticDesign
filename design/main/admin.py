from django.contrib import admin
from .models import Claim, Category


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_time', 'user']
    list_filter = ['status', 'created_time']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['name', 'description', 'category', 'created_time', 'user', 'photo']
    fields = ['name', 'description', 'category', 'status', 'created_time', 'user', 'photo']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

    # def change_status(self, request, queryset):
    #     for claim in queryset:
    #         if claim.status == 'accepted':
    #






@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']