from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    # url(r'^django-admin/django-ses/', include('django_ses.urls')),

    path(r'', include('apps.auth_user.urls')),
    path(r'', include('apps.pool_shop.urls')),

    # Site map
    url(r'^BingSiteAuth\.xml$', TemplateView.as_view(template_name='./BingSiteAuth.xml',  # File in template folder
                                                     content_type='text/xml; charset=utf-8')),

    url(r'404/$', TemplateView.as_view(template_name='404.html'), name='404'),
    url(r'500/$', TemplateView.as_view(template_name='500.html'), name='500'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os

    urlpatterns += static(r'maintenance/', document_root=os.path.join(settings.BASE_DIR, 'templates', 'maintenance'))

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
