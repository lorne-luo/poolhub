from django import forms
from django.forms import ModelForm

from apps.training.models import TrainTesting


class TrainTestingCreateForm(ModelForm):
    class Meta:
        model = TrainTesting
        fields = ['original_image', 'th_value', 'tc_value', 'fc_value', 'ph_value', 'ta_value', 'ca_value']
