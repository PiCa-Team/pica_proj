from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path("", views.home, name="home"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('recorded_videos/', views.recorded_videos, name='recorded_videos'),
    path('recorded_videos_detail/<str:video_name>/', views.recorded_videos_detail, name='video_detail'),
]
