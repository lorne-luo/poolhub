from django import forms
from django.forms import ModelForm

from apps.testing.models import Testing, TrainTesting


class TestingCreateForm(ModelForm):
    class Meta:
        model = Testing
        fields = ['image']


class TrainTestingCreateForm(ModelForm):
    class Meta:
        model = TrainTesting
        fields = ['image', 'th_value', 'tc_value', 'fc_value', 'ph_value', 'ta_value', 'ca_value']
