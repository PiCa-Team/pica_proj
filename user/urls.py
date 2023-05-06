from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path("", views.MyLoginView.as_view(), name="login"),
                  path("logout/", views.logout_view, name="logout"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
