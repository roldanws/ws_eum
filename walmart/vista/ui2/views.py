from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class UiPageView(TemplateView):
    template_name = "ui/ui.html"	