from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView


class DashboardView(TemplateView):
    template_name = 'pool_shop/dashboard.html'
