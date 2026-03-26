from django.db import models
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField()
    score = models.IntegerField(default=0)
    depth = models.PositiveSmallIntegerField(default=0)  # 0, 1, 2 max
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.parent:
            self.depth = min(self.parent.depth + 1, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
