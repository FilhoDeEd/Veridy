from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class SubjectRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        label='Nome completo',
        max_length=255,
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )

    # birth_date = forms.DateField(
    #     label='Data de nascimento',
    #     widget=forms.DateInput(
    #         attrs={'type': 'date'}
    #     ),
    #     required=False
    # )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'exemplo@exemplo.edu.br'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)
