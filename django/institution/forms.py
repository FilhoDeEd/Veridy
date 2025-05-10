from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class InstitutionRegistrationForm(UserCreationForm):
    name = forms.CharField(label='Nome', max_length=255)
    tax_id = forms.CharField(label='CNPJ ou equivalente', max_length=255)
    domain = forms.CharField(label='Domínio institucional', max_length=255, help_text='ex: exemplo.edu.br')
    institutional_email = forms.EmailField(label='E-mail institucional')
    phone = forms.CharField(label='Telefone de contato', max_length=20)

    city = forms.CharField(label='Cidade', max_length=255)
    state = forms.CharField(label='Estado', max_length=255)
    country = forms.CharField(label='País', max_length=255)
    full_address = forms.CharField(
        label='Endereço completo',
        widget=forms.Textarea(attrs={'rows': 3})
    )

    representative_name = forms.CharField(label='Nome', max_length=255)
    representative_role = forms.CharField(label='Cargo', max_length=255)
    representative_email = forms.EmailField(label='E-mail')
    representative_phone = forms.CharField(label='Telefone', max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
