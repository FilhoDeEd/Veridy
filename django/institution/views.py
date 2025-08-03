from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, TemplateView, View

from django_filters.views import FilterView

from institution.forms import (
    DomainInputForm,
    InstitutionEditAddressForm,
    InstitutionEditBasicForm,
    InstitutionRegistrationForm,
    LegalRepresentativeForm
)
from institution.mixins import InstitutionRequiredMixin
from institution.models import DomainVerificationToken, Institution, LegalRepresentative
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


class InstitutionEditBasicView(InstitutionRequiredMixin, FormView):
    template_name = 'institution_edit_basic.html'
    form_class = InstitutionEditBasicForm
    success_url = reverse_lazy('institution_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.institution = self.request.user.institution
        kwargs['instance'] = self.institution
        return kwargs

    def form_valid(self, form: InstitutionEditBasicForm):
        form.save()
        messages.success(self.request, 'Dados básicos atualizados com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)


class InstitutionEditAddressView(InstitutionRequiredMixin, FormView):
    template_name = 'institution_edit_address.html'
    form_class = InstitutionEditAddressForm
    success_url = reverse_lazy('institution_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.institution = self.request.user.institution
        kwargs['instance'] = self.institution
        return kwargs

    def form_valid(self, form: InstitutionEditAddressForm):
        form.save()
        messages.success(self.request, 'Endereço atualizado com sucesso!')
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
        kwargs = super().get_form_kwargs()
        self.institution = self.request.user.institution
        kwargs['instance'] = self.institution.representative
        return kwargs

    def form_valid(self, form: LegalRepresentativeForm):
        representative = form.save()
        self.institution.representative = representative
        self.institution.save()
        messages.success(self.request, 'Responsável legal atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)


class InstitutionVerificationRequestTokenView(InstitutionRequiredMixin, FormView):
    template_name = 'institution_verification/request_token.html'
    form_class = DomainInputForm
    success_url = reverse_lazy('verification_display_token')

    def dispatch(self, request, *args, **kwargs):
        self.institution: Institution = request.user.institution
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.institution.is_verified:
            messages.warning(
                request,
                'Esta instituição já está verificada. Ao iniciar um novo processo de verificação, '
                'o status da instituição voltará para pendente até que a verificação seja concluída. '
                'Certifique-se de que essa alteração é necessária.'
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: DomainInputForm):
        try:
            self.domain = self.institution.domain
            unverified_domain = form.cleaned_data['domain'].strip().lower()

            if self.institution.is_verified and unverified_domain == self.domain:
                form.add_error('domain', 'O novo domínio deve ser diferente do domínio atual já verificado.')
                return self.form_invalid(form)

            with transaction.atomic():
                self.institution.unverify()
                self.institution.save()

                DomainVerificationToken.objects.filter(institution=self.institution).delete()

                token = DomainVerificationToken.objects.create(
                    temporary_domain=unverified_domain,
                    institution=self.institution
                )
                token.save()

                messages.success(self.request, 'Token de verificação gerado com sucesso! Prossiga com a validação.')
        except Exception:
            messages.error(self.request, 'Erro ao gerar token de verificação. Por favor, tente novamente.')
            return self.form_invalid(form)

        return super().form_valid(form)


class InstitutionVerificationDisplayTokenView(InstitutionRequiredMixin, DetailView):
    model = DomainVerificationToken
    template_name = 'institution_verification/display_token.html'
    context_object_name = 'token'

    def get_object(self, queryset=None):
        institution = self.request.user.institution
        try:
            return DomainVerificationToken.objects.get(institution=institution)
        except DomainVerificationToken.DoesNotExist:
            raise Http404('Nenhum token de verificação encontrado.')


class InstitutionVerificationDownloadTokenView(InstitutionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        institution = self.request.user.institution

        try:
            token = DomainVerificationToken.objects.get(institution=institution)
        except DomainVerificationToken.DoesNotExist:
            raise Http404('Token de verificação não encontrado.')

        content = token.token
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=verificacao_{institution.id}.txt'
        return response

# class DomainVerificationView(InstitutionRequiredMixin, FormView):
#     template_name = 'institution_verify.html'
#     form_class = DomainForm
#     success_url = reverse_lazy('institution_profile')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         institution = self.request.user.institution

#         token, _ = DomainVerificationToken.objects.get_or_create(institution=institution)
#         if token.is_expired():
#             token.delete()
#             token = DomainVerificationToken.objects.create(institution=institution)

#         context['token'] = token.token
#         context['expires_at'] = token.expiration_date
#         return context

#     def form_valid(self, form: DomainForm):
#         data = form.cleaned_data
#         institution: Institution = self.request.user.institution

#         try:
#             with transaction.atomic():
#                 token, _ = DomainVerificationToken.objects.get_or_create(institution=institution)
#                 if token.is_expired():
#                     token.delete()
#                     token = DomainVerificationToken.objects.create(institution=institution)
#                 institution.domain = data['domain']
#         except Exception:
#             messages.error(self.request, 'Erro ao gerar token de verificação. Por favor, tente novamente.')
#             return self.form_invalid(form)

#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return super().form_invalid(form)

#     def post(self, request, *args, **kwargs):
#         institution = self.request.user.institution
#         token_obj = getattr(institution, 'verification_token', None)

#         if not token_obj or token_obj.is_expired():
#             messages.error(request, "O token expirou. Um novo token será gerado.")
#             return redirect('institution_start_verification')

#         try:
#             answers = dns.resolver.resolve(institution.domain, 'TXT')
#             for rdata in answers:
#                 if token_obj.token in str(rdata):
#                     institution.domain_verified = True
#                     institution.domain_verification_date = timezone.now()
#                     institution.status = institution.Status.VERIFIED
#                     institution.save()
#                     token_obj.delete()
#                     messages.success(request, "Domínio verificado com sucesso!")
#                     return redirect('institution_profile')
#             messages.error(request, "Token não encontrado nos registros DNS. Verifique e tente novamente.")
#         except Exception as e:
#             messages.error(request, f"Erro ao consultar DNS: {e}")

#         return redirect('institution_start_verification')
