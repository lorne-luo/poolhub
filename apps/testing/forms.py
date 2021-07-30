from django import forms
from django.forms import ModelForm

from apps.testing.models import Testing


class TestingCreateForm(ModelForm):
    class Meta:
        model = Testing
        fields = ['original_image']

