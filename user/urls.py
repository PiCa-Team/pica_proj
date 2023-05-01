from django.urls import path
from . import views

urlpatterns = [
    path("", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]