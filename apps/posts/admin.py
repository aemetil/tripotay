from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'score', 'comment_count', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('score', 'comment_count', 'slug', 'created_at', 'updated_at')
    list_editable = ('status',)
