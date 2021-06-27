from django.conf.urls import url
from django.urls import path, include

from apps.testing import views

urlpatterns = [
    url('testing/train_stripe_upload/', views.TrainStripUploadView.as_view(), name='poolshop_dashboard'),
    url('testing/stripe_upload/', views.StripUploadView.as_view(), name='poolshop_dashboard'),
]
