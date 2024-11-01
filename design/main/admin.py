from django.contrib import admin

from .models import Category, Claim

# admin.site.register(Category)
# admin.site.register(Claim)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

