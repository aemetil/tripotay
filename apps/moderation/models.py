from django.db import models
from django.conf import settings
from django.utils import timezone


class BlockedWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word


class Report(models.Model):

    class Reason(models.TextChoices):
        OFFENSIVE = 'offensive', 'Offensive / insulte'
        SPAM = 'spam', 'Spam'
        MISINFORMATION = 'misinformation', 'Fausse information'
        OTHER = 'other', 'Autre'

    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        REVIEWED = 'reviewed', 'Vérifié'
        DISMISSED = 'dismissed', 'Ignoré'

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports_made'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports'
    )
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports'
    )
    reason = models.CharField(max_length=20, choices=Reason.choices)
    detail = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    auto_publish_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        target = f'post {self.post_id}' if self.post_id else f'comment {self.comment_id}'
        return f'Report on {target} by {self.reporter}'
