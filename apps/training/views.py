from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, CreateView, DetailView

from apps.training.forms import  TrainTestingCreateForm
from apps.training.models import  TrainTesting


class TrainStripUploadView(CreateView):
    template_name = 'training/train_stripe_upload.html'
    form_class = TrainTestingCreateForm
    model = TrainTesting

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('train_stripe_detail',args=[self.object.id])

class TrainStripDetailView(DetailView):
    template_name = 'training/train_stripe_detail.html'
    model = TrainTesting
