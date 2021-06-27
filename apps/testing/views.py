from django.shortcuts import render
from django.views.generic import FormView, CreateView

from apps.testing.forms import TestingCreateForm, TrainTestingCreateForm
from apps.testing.models import Testing


class TrainStripUploadView(CreateView):
    template_name = 'testing/train_stripe_upload.html'
    form_class = TrainTestingCreateForm
    model = Testing
    # fields = ['name']


class StripUploadView(CreateView):
    template_name = 'testing/stripe_upload.html'
    form_class = TestingCreateForm
    model = Testing
