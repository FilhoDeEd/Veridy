from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import InstitutionRegistrationForm, InstitutionEditForm
from .models import Institution, LegalRepresentative


class InstitutionProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'institution_profille.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['institution'] = self.request.user.institution
        return self.render_to_response(context)


class InstitutionRegistrationView(FormView):
    template_name = 'institution_registration.html'
    form_class = InstitutionRegistrationForm
    success_url = reverse_lazy('home') #reverse_lazy('institution_list')

    def form_valid(self, form: InstitutionRegistrationForm):
        data = form.cleaned_data
        institutional_email = data.get('institutional_email')

        if Institution.objects.filter(institutional_email=institutional_email).exists():
            form.add_error('institutional_email', 'Uma instituição com este e-mail já está cadastrada.')
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=data.get('username'),
                    email=None,
                    password=data.get('password1')
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
                    institutional_email=data.get('institutional_email'),
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


class InstitutionEditView(LoginRequiredMixin, FormView):
    template_name = 'institution_edit.html'
    form_class = InstitutionEditForm
    success_url = reverse_lazy('institution_profile')  # Atualize com sua URL

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