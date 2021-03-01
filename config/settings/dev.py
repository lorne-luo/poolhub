from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='27ccw6=vv%*m=0+u)duqrtby6!nzw$f(l7v(!in1hxm129)+du')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '.butterfly.com.au', ])

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS += ['django_extensions']

try:
    from .local import *
except ImportError:
    pass

try:
    # declare DEV_APPS in local.py if you have extra apps personally
    INSTALLED_APPS += DEV_APPS
except NameError:
    pass
