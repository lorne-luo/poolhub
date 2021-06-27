from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView

from apps.testing.forms import TestingCreateForm, TrainTestingCreateForm
from apps.testing.models import Testing, TrainTesting


class TrainStripUploadView(CreateView):
    template_name = 'testing/train_stripe_upload.html'
    form_class = TrainTestingCreateForm
    model = TrainTesting

    def get_success_url(self):
        return reverse('testing-train_stripe_detail',args=[self.object.id])

class TrainStripDetailView(DetailView):
    template_name = 'testing/train_stripe_detail.html'
    model = TrainTesting


class StripUploadView(CreateView):
    template_name = 'testing/stripe_upload.html'
    form_class = TestingCreateForm
    model = Testing


class StripDetailView(DetailView):
    template_name = 'testing/stripe_detail.html'
    model = Testing
