from django import forms
from django.contrib.auth.models import User
from .models import models

class UserForms(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    class Meta():
        model = User
        fields = ('first_name', 'username', 'cpf_cnpj', 'tipo','password')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
