from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.posts.models import Post
from apps.moderation.models import Report


class Command(BaseCommand):
    help = 'Publie automatiquement les posts en attente depuis plus de 24h sans action admin'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Posts en pending_review dont le signalement auto a dépassé 24h
        expired_reports = Report.objects.filter(
            status=Report.Status.PENDING,
            auto_publish_at__isnull=False,
            auto_publish_at__lte=now,
            post__status='pending_review',
        ).select_related('post')

        count = 0
        for report in expired_reports:
            report.post.status = Post.Status.PUBLISHED
            report.post.save(update_fields=['status'])
            report.status = Report.Status.DISMISSED
            report.save(update_fields=['status'])
            count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} post(s) auto-publiés.'))
