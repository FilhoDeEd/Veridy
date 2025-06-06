from common.models import UserTypeChoices

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django_filters.views import FilterView

from document.forms import DocumentUploadForm
from institution.mixins import InstitutionRequiredMixin
from document.models import Document
from institution.filters import InstitutionFilter


class DocumentUploadView(InstitutionRequiredMixin, FormView):
    template_name = 'document_upload.html'
    form_class = DocumentUploadForm
    success_url = reverse_lazy('home')

    def form_valid(self, form: DocumentUploadForm):
        data = form.cleaned_data
        institution = self.request.user.institution

        try:
            with transaction.atomic():
                Document.objects.create(
                    file=data.get('file'),
                    subject=data.get('subject'),
                    institution=institution
                )
            messages.success(self.request, 'Certificado enviado com sucesso!')
        except Exception:
            messages.error(self.request, 'Ocorreu um erro ao processar o certificado. Tente novamente.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao enviar o formulário. Verifique os campos e tente novamente.')
        return super().form_invalid(form)
