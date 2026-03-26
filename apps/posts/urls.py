from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExploreView.as_view(), name='explore'),
    path('ekri/', views.PostCreateView.as_view(), name='post_create'),
    path('p/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
