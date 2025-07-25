from django import forms
from django.contrib.auth.forms import UserCreationForm
from institution.models import Institution, LegalRepresentative
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class InstitutionRegistrationForm(UserCreationForm):
    name = forms.CharField(
        label='Nome da Instituição',
        max_length=255,
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'E-mail da Instituição'}
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'exemplo@exemplo.edu.br'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})


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

    # email = forms.EmailField(
    #     label='E-mail Institucional',
    #     widget=forms.EmailInput(
    #         attrs={'placeholder': 'e.g. contato@ufpe.br'})
    # )

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
            # 'email',
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
