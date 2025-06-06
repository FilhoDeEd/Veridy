from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django_filters.views import FilterView

from subject.forms import SubjectEditForm, SubjectRegistrationForm
from subject.mixins import SubjectRequiredMixin
from subject.models import Subject
from subject.filters import SubjectFilter


UserModel = get_user_model()


class SubjectListView(FilterView):
    model = Subject
    template_name = 'subject_list.html'
    filterset_class = SubjectFilter
    context_object_name = 'subjects'
    ordering = ['full_name']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'subject'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__is_active=True)


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


class SubjectProfileView(SubjectRequiredMixin, TemplateView):
    template_name = 'subject_profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['subject'] = self.request.user.subject
        return self.render_to_response(context)


class SubjectEditView(SubjectRequiredMixin, FormView):
    template_name = 'subject_edit.html'
    form_class = SubjectEditForm
    success_url = reverse_lazy('subject_profile')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        self.subject = self.request.user.subject
        form_kwargs.update({'instance': self.subject})
        return form_kwargs

    def form_valid(self, form: SubjectEditForm):
        form.save()
        messages.success(self.request, 'Dados atualizados com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)
