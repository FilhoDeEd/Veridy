from django import forms
from django.template.defaultfilters import filesizeformat

from document.models import Document

from subject.models import Subject


MAX_BYTES_FILE = 5 * 1024 * 1024
ALLOWED_CONTENT_TYPES = ['application/pdf']


class DocumentUploadForm(forms.ModelForm):
    file = forms.FileField(
        label='Arquivo PDF'
    )

    subject = forms.ModelChoiceField(
        label='Titular',
        queryset=Subject.objects.filter(user__is_active=True)
    )

    class Meta:
        model = Document
        fields = ['file', 'subject']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Este campo é obrigatório.')

        if file.size > MAX_BYTES_FILE:
            raise forms.ValidationError(
                f'O tamanho máximo para o arquivo é de {filesizeformat(MAX_BYTES_FILE)}. '
                f'O arquivo atual possui {filesizeformat(file.size)}.'
            )

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError('Tipo de arquivo não permitido. Envie apenas arquivos PDF.')

        return file
