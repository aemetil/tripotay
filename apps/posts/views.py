from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from apps.categories.models import Category
from apps.comments.models import Comment
from apps.comments.forms import CommentForm


class ExploreView(ListView):
    model = Post
    template_name = 'posts/explore.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return (
            Post.objects
            .filter(status=Post.Status.PUBLISHED)
            .select_related('author', 'category')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = (
            Comment.objects
            .filter(post=self.object, parent=None)
            .select_related('author')
            .prefetch_related('replies__author', 'replies__replies__author')
            .order_by('created_at')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('explore')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        from apps.moderation.services import check_post_for_moderation
        check_post_for_moderation(self.object)
        return response
