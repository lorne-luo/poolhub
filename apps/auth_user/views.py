from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import logout
from django.conf import settings
from django.db import connection
from django_tenants.utils import get_public_schema_name

from core.constants import UserRole


class AuthLoginView(LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        current_schema_name = connection.tenant.schema_name
        public_schema_name = get_public_schema_name()

        if self.request.user.role == UserRole.SHOP_MANAGER:
            # poolshop manager, to shop dashboard
            default_redirect_url = f"/{settings.TENANT_SUBFOLDER_PREFIX}/{self.request.user.tenant.schema_name}/shop/dashboard"
            if url and not url.startswith(f"/{settings.TENANT_SUBFOLDER_PREFIX}/{self.request.user.tenant.schema_name}"):
                url = f"/{settings.TENANT_SUBFOLDER_PREFIX}/{self.request.user.tenant.schema_name}{url}"
        elif self.request.user.role == UserRole.CUSTOMER:
            # todo customer login
            default_redirect_url = "/"
        elif self.request.user.role == UserRole.SUPER_ADMIN:
            default_redirect_url = "/django-admin/"
        else:
            default_redirect_url = resolve_url(settings.LOGIN_REDIRECT_URL)
        return url or default_redirect_url


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
