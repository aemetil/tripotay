from django.urls import path
from . import views

urlpatterns = [
    path('p/<int:post_pk>/komante/', views.add_comment, name='add_comment'),
]
