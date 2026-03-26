from django.urls import path
from . import views

urlpatterns = [
    path('p/<int:post_pk>/rapote/', views.report_post, name='report_post'),
]
