from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django_filters.views import FilterView

from subject.forms import SubjectRegistrationForm
# from subject.mixins import InstitutionRequiredMixin
from subject.models import Subject
# from subject.filters import InstitutionFilter


UserModel = get_user_model()


class SubjectRegistrationView(FormView):
    template_name = 'subject_registration.html'
    form_class = SubjectRegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'subject'
        return context

    def form_valid(self, form: SubjectRegistrationForm):
        data = form.cleaned_data

        try:
            with transaction.atomic():
                user = UserModel.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password1'),
                    user_type=UserTypeChoices.SUBJECT
                )

                Subject.objects.create(
                    user=user,
                    full_name=data.get('full_name')
                )

            messages.success(self.request, 'Cadastro realizado com sucesso!')
        except Exception:
            messages.error(self.request, 'Erro ao cadastrar. Por favor, tente novamente.')
            return self.form_invalid(form)

        return super().form_valid(form)
