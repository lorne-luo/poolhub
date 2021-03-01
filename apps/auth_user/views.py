from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.conf import settings


class AuthLoginView(LoginView):
    template_name = 'auth/login.html'


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
