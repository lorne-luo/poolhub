from django.conf.urls import url
from django.urls import path, include

from apps.pool_shop import views

app_name = 'pool_shop'

urlpatterns = [
    url('shop/dashboard/', views.DashboardView.as_view(), name='poolshop_dashboard'),
]
