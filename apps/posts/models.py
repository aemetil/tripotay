from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Published'
        PENDING = 'pending_review', 'Pending review'
        REMOVED = 'removed', 'Removed'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='posts'
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, blank=True)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED
    )
    score = models.IntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:320]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
