from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.posts.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.comments.urls')),
    path('', include('apps.votes.urls')),
    path('', include('apps.moderation.urls')),
]
