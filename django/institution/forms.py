from django import forms
from django.contrib.auth.forms import UserCreationForm
from institution.models import Institution, LegalRepresentative
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class InstitutionRegistrationForm(UserCreationForm):
    name = forms.CharField(label='Nome', max_length=255)
    tax_id = forms.CharField(label='CNPJ ou equivalente', max_length=255)
    domain = forms.CharField(label='Domínio institucional', max_length=255, help_text='ex: exemplo.edu.br')
    phone = forms.CharField(label='Telefone de contato', max_length=20)

    city = forms.CharField(label='Cidade', max_length=255)
    state = forms.CharField(label='Estado', max_length=255)
    country = forms.CharField(label='País', max_length=255)
    full_address = forms.CharField(
        label='Endereço completo',
        widget=forms.Textarea(attrs={'rows': 2})
    )

    representative_name = forms.CharField(label='Nome', max_length=255)
    representative_role = forms.CharField(label='Cargo', max_length=255)
    representative_email = forms.EmailField(label='E-mail')
    representative_phone = forms.CharField(label='Telefone', max_length=20)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class InstitutionEditForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome da Instituição',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Universidade Federal de Pernambuco'})
    )

    tax_id = forms.CharField(
        label='CNPJ',
        max_length=18,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. 12.345.678/0001-90'})
    )

    domain = forms.CharField(
        label='Domínio Institucional',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. ufpe.br'})
    )

    institutional_email = forms.EmailField(
        label='E-mail Institucional',
        widget=forms.EmailInput(
            attrs={'placeholder': 'e.g. contato@ufpe.br'})
    )

    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. (81) 2126-8000'})
    )

    city = forms.CharField(
        label='Cidade',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Recife'})
    )

    state = forms.CharField(
        label='Estado',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. CE'})
    )

    country = forms.CharField(
        label='País',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Brasil'})
    )

    full_address = forms.CharField(
        label='Endereço Completo',
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Av. Prof. Moraes Rego, 1235 - Cidade Universitária'})
    )

    class Meta:
        model = Institution
        fields = [
            'name',
            'tax_id',
            'domain',
            'institutional_email',
            'phone',
            'city',
            'state',
            'country',
            'full_address'
        ]

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        return tax_id.replace('.', '').replace('/', '').replace('-', '') if tax_id else None


class LegalRepresentativeForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome do Responsável Legal',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. João Silva'})
    )

    role = forms.CharField(
        label='Cargo',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Diretor'})
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'e.g. joao.silva@example.com'})
    )

    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. (11) 91234-5678'})
    )

    class Meta:
        model = LegalRepresentative
        fields = ['name', 'role', 'email', 'phone']
