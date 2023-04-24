from django import forms
from django.contrib.auth.models import User
from . models import models

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

    def clean(self, *args, **kwargs):
        validation_error_msgs = {}


        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        email = self.cleaned_data.get('username')
        password_data =self.cleaned_data.get('password')
        nome = self.cleaned_data.get('first_name')

        usuario_db = User.objects.filter(username=email).first()
        print(nome)
        if not nome:
            validation_error_msgs['first_name'] = error_msg_required_field

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))