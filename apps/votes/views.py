from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from apps.posts.models import Post
from apps.users.models import User
from .models import PostVote


@login_required
@require_POST
def vote_post(request, post_pk):
    try:
        value = int(request.POST.get('value', 1))
        if value not in (1, -1):
            return JsonResponse({'error': 'invalid'}, status=400)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'invalid'}, status=400)

    post = Post.objects.filter(pk=post_pk, status=Post.Status.PUBLISHED).first()
    if not post:
        return JsonResponse({'error': 'not found'}, status=404)

    existing = PostVote.objects.filter(user=request.user, post=post).first()

    with transaction.atomic():
        if existing:
            if existing.value == value:
                # Même vote → on retire (toggle off)
                delta = -value
                existing.delete()
                user_voted = 0
            else:
                # Vote opposé → on change
                delta = value - existing.value
                existing.value = value
                existing.save()
                user_voted = value
        else:
            # Nouveau vote
            delta = value
            PostVote.objects.create(user=request.user, post=post, value=value)
            user_voted = value

        # Mise à jour score post et karma auteur avec F()
        Post.objects.filter(pk=post.pk).update(score=F('score') + delta)
        if post.author_id and post.author_id != request.user.pk:
            User.objects.filter(pk=post.author_id).update(karma=F('karma') + delta)

    post.refresh_from_db()
    return JsonResponse({'score': post.score, 'user_voted': user_voted})
