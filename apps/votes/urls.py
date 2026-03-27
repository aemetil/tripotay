from django.urls import path
from . import views

urlpatterns = [
    path('p/<int:post_pk>/vote/', views.vote_post, name='vote_post'),
]
