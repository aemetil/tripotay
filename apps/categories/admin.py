from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)
