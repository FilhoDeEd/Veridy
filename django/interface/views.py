from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'home.html'
