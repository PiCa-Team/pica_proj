from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

# Create your views here.


class MyLoginView(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect("login")
