from django.conf.urls import url
from django.urls import path, include

from apps.auth_user.views import AuthLoginView, logout_view

app_name = 'auth_user'

urlpatterns = [
    url('login/', AuthLoginView.as_view(), name='login'),
    url('logout/', logout_view, name='logout'),
]
