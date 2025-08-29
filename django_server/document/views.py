from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from django_filters.views import FilterView

from document.forms import DocumentUploadForm
from document.models import Document
from document.filters import DocumentFilter

from institution.mixins import InstitutionRequiredMixin

from ipfs_api import ipfshttpclient


class DocumentListView(FilterView):
    model = Document
    template_name = 'document_list.html'
    filterset_class = DocumentFilter
    context_object_name = 'documents'
    ordering = ['-upload_date']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_type'] = 'document'
        return context


class DocumentUploadView(InstitutionRequiredMixin, FormView):
    template_name = 'document_upload.html'
    form_class = DocumentUploadForm
    success_url = reverse_lazy('home')

    def form_valid(self, form: DocumentUploadForm):
        data = form.cleaned_data
        institution = self.request.user.institution

        try:
            with transaction.atomic():
                document = Document.objects.create(
                    file=data.get('file'),
                    subject=data.get('subject'),
                    institution=institution
                )

                client = ipfshttpclient.connect()
                res = client.add(document.file.path)
                ipfs_cid = res['Hash']

                document.ipfs_cid = ipfs_cid
                document.save()

            messages.success(self.request, 'Certificado enviado com sucesso!')
        except Exception as e:
            print(e)
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu um erro ao processar o certificado. Tente novamente.')
        return super().form_invalid(form)


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document_detail.html'
    context_object_name = 'document'
    pk_url_kwarg = 'document_id'
