from django import forms
from django.contrib.auth.forms import UserCreationForm
from institution.models import Institution, LegalRepresentative
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class InstitutionRegistrationForm(UserCreationForm):
    name = forms.CharField(
        label='Nome',
        max_length=255,
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )

    acronym = forms.CharField(
        label='Sigla',
        max_length=255,
        required=False,
        widget=forms.TextInput()
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'E-mail da Instituição'}
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'exemplo@exemplo.edu.br'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})


class InstitutionEditBasicForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome da Instituição',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Universidade de São Paulo'}
        )
    )

    acronym = forms.CharField(
        label='Sigla',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. USP'}
        )
    )

    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. (81) 2126-8000'}
        )
    )

    class Meta:
        model = Institution
        fields = [
            'name',
            'acronym',
            'phone'
        ]


class InstitutionEditAddressForm(forms.ModelForm):
    city = forms.CharField(
        label='Cidade',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. São Paulo'}
        )
    )

    state = forms.CharField(
        label='Estado',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. SP'}
        )
    )

    country = forms.CharField(
        label='País',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Brasil'}
        )
    )

    full_address = forms.CharField(
        label='Endereço Completo',
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'placeholder': 'e.g. R. da Reitoria, 374 - Butantã, São Paulo - SP, 05508-220'
            }
        )
    )

    class Meta:
        model = Institution
        fields = [
            'city',
            'state',
            'country',
            'full_address'
        ]


class LegalRepresentativeForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. João Silva'}
        )
    )

    role = forms.CharField(
        label='Cargo',
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Diretor'})
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={'placeholder': 'e.g. joao.silva@example.com'}
        )
    )

    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. (11) 91234-5678'}
        )
    )

    class Meta:
        model = LegalRepresentative
        fields = [
            'name',
            'role',
            'email',
            'phone'
        ]


class DomainInputForm(forms.Form):
    domain = forms.CharField(
        label='Domínio Institucional',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. exemplo.edu.br'}
        )
    )
