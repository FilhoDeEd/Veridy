from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, TemplateView

from django_filters.views import FilterView

from institution.forms import InstitutionEditForm, InstitutionRegistrationForm, LegalRepresentativeForm
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

    # Colocar em Subject tbm
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'institution'
        return context

    def form_valid(self, form: InstitutionRegistrationForm):
        data = form.cleaned_data

        try:
            with transaction.atomic():
                user = UserModel.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password1'],
                    user_type=UserTypeChoices.INSTITUTION
                )
                institution = Institution.objects.create(
                    user=user,
                    name=data['name'],
                    acronym=data['acronym']
                )
                institution.save()

            username = data['username']
            password = data['password1']
            auth_user = authenticate(self.request, username=username, password=password)
            login(self.request, auth_user)

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


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'institution_detail.html'
    pk_url_kwarg = 'institution_id'
    context_object_name = 'institution'

    def get_object(self, queryset=None):
        institution = super().get_object()
        if not institution.user.is_active:
            raise Http404('Instituição não encontrada.')
        return institution


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
