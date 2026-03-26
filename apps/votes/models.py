from django.db import models
from django.conf import settings


class PostVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_votes'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    value = models.SmallIntegerField()  # +1 ou -1

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} → post {self.post_id} ({self.value:+d})'


class CommentVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_votes'
    )
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    value = models.SmallIntegerField()  # +1 ou -1

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user} → comment {self.comment_id} ({self.value:+d})'
