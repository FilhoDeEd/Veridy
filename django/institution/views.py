from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django_filters.views import FilterView

from institution.forms import InstitutionRegistrationForm, InstitutionEditForm, LegalRepresentativeForm
from institution.mixins import InstitutionRequiredMixin
from institution.models import Institution, LegalRepresentative
from institution.filters import InstitutionFilter


UserModel = get_user_model()


class InstitutionListView(FilterView):
    model = Institution
    template_name = 'institution_list.html'
    filterset_class = InstitutionFilter
    context_object_name = 'institutions'
    ordering = ['name']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'institution'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__is_active=True)


class InstitutionRegistrationView(FormView):
    template_name = 'institution_registration.html'
    form_class = InstitutionRegistrationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'institution'
        return context

    def form_valid(self, form: InstitutionRegistrationForm):
        data = form.cleaned_data

        try:
            with transaction.atomic():
                user = UserModel.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password1'),
                    user_type=UserTypeChoices.INSTITUTION
                )

                representative = LegalRepresentative.objects.create(
                    name=data.get('representative_name'),
                    role=data.get('representative_role'),
                    email=data.get('representative_email'),
                    phone=data.get('representative_phone')
                )

                Institution.objects.create(
                    user=user,
                    name=data.get('name'),
                    tax_id=data.get('tax_id'),
                    domain=data.get('domain'),
                    phone=data.get('phone'),
                    city=data.get('city'),
                    state=data.get('state'),
                    country=data.get('country'),
                    full_address=data.get('full_address'),
                    representative=representative
                )

            messages.success(self.request, 'Instituição cadastrada com sucesso!')
        except Exception:
            messages.error(self.request, 'Erro ao cadastrar a instituição. Por favor, tente novamente.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class InstitutionProfileView(InstitutionRequiredMixin, TemplateView):
    template_name = 'institution_profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['institution'] = self.request.user.institution
        return self.render_to_response(context)


class InstitutionEditView(InstitutionRequiredMixin, FormView):
    template_name = 'institution_edit.html'
    form_class = InstitutionEditForm
    success_url = reverse_lazy('institution_profile')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        self.institution = self.request.user.institution
        form_kwargs.update({'instance': self.institution})
        return form_kwargs

    def form_valid(self, form: InstitutionEditForm):
        institutional_email = form.cleaned_data.get('institutional_email')

        if Institution.objects.filter(institutional_email=institutional_email).exclude(id=self.institution.id).exists():
            form.add_error('institutional_email', 'Uma instituição com este e-mail já está cadastrada.')
            return self.form_invalid(form)

        tax_id = form.cleaned_data.get('tax_id')
        if Institution.objects.filter(tax_id=tax_id).exclude(id=self.institution.id).exists():
            form.add_error('tax_id', 'Uma instituição com este CNPJ já está cadastrada.')
            return self.form_invalid(form)

        form.save()
        messages.success(self.request, 'Dados da instituição atualizados com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)


class LegalRepresentativeEditView(InstitutionRequiredMixin, FormView):
    template_name = 'legal_representative_edit.html'
    form_class = LegalRepresentativeForm
    success_url = reverse_lazy('institution_profile')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        self.institution = self.request.user.institution
        self.representative = self.institution.representative
        form_kwargs.update({'instance': self.representative})
        return form_kwargs

    def form_valid(self, form: LegalRepresentativeForm):
        form.save()
        messages.success(self.request, 'Dados do responsável legal atualizados com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)
