from django.contrib import admin
from .models import BlockedWord, Report


@admin.register(BlockedWord)
class BlockedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'created_by', 'created_at')
    search_fields = ('word',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'post', 'comment', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
