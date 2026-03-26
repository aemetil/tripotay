from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from apps.posts.models import Post
from .models import Comment
from .forms import CommentForm


@login_required
@require_POST
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)

    if form.is_valid():
        parent_id = request.POST.get('parent_id')
        parent = None

        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id, post=post)
            # max depth 2
            if parent.depth >= 2:
                parent = parent.parent

        with transaction.atomic():
            Comment.objects.create(
                post=post,
                author=request.user,
                parent=parent,
                content=form.cleaned_data['content'],
            )
            Post.objects.filter(pk=post.pk).update(
                comment_count=post.comment_count + 1
            )

    return redirect('post_detail', pk=post_pk)
