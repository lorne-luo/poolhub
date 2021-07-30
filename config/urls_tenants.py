from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
    path(r'django-admin/', admin.site.urls),
    path(r'testing/', include('apps.testing.urls', namespace='testing')),
    #
    # path(r'shop/', include('apps.pool_shop.urls')),
    # # path('', include('apps.payment.urls')),
    # url(r'405/$', TemplateView.as_view(template_name='404.html'), name='405'),

]
