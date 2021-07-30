from django.conf.urls import url
from django.urls import path, include, reverse

from apps.training import views

app_name = 'training'

urlpatterns = [
    # train upload
    path(r'stripe_upload/<int:pk>/', views.TrainStripDetailView.as_view(), name='stripe_detail'),
    path(r'stripe_upload/', views.TrainStripUploadView.as_view(), name='stripe_upload'),
]
