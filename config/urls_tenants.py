from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    path('', include('apps.auth_user.urls')),

    # path('', include('apps.customer.urls')),
    # path('', include('apps.payment.urls')),
]

