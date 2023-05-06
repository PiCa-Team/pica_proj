from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recorded_videos/', views.recorded_videos, name='recorded_videos'),
    path('recorded_videos_detail/<str:video_name>/', views.recorded_videos_detail, name='video_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
