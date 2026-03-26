from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.posts.models import Post
from apps.comments.models import Comment
from .models import Report


@login_required
@require_POST
def report_post(request, post_pk):
    post = Post.objects.filter(pk=post_pk).first()
    if not post:
        return JsonResponse({'error': 'not found'}, status=404)

    reason = request.POST.get('reason', 'other')
    if reason not in dict(Report.Reason.choices):
        reason = 'other'

    # Un seul signalement par user/post
    already = Report.objects.filter(reporter=request.user, post=post).exists()
    if already:
        return JsonResponse({'status': 'already_reported'})

    Report.objects.create(
        reporter=request.user,
        post=post,
        reason=reason,
    )
    return JsonResponse({'status': 'reported'})
