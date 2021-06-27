from django.conf.urls import url
from django.urls import path, include, reverse

from apps.testing import views

urlpatterns = [
    path(r'testing/train_stripe_upload/<int:pk>/', views.TrainStripDetailView.as_view(),
         name='testing-train_stripe_detail'),
    url(r'testing/train_stripe_upload/', views.TrainStripUploadView.as_view(), name='testing-train_stripe_upload'),

    path(r'testing/stripe_upload/<int:pk>/', views.StripDetailView.as_view(),
         name='testing-stripe_view_detail'),
    url(r'testing/stripe_upload/', views.StripUploadView.as_view(), name='testing-stripe_upload'),
]
