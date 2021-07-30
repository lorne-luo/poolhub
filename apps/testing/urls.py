from django.conf.urls import url
from django.urls import path, include, reverse

from apps.testing import views

app_name = 'testing'

urlpatterns = [
    # tenant stripe upload
    path(r'stripe_upload/<int:pk>/', views.StripDetailView.as_view(), name='stripe_detail'),
    path(r'stripe_upload/', views.StripUploadView.as_view(), name='stripe_upload'),

]
