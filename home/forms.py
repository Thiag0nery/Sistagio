from django import forms
from django.contrib.auth.models import User
from perfil.models import PerfilUser
class UserForms(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    class Meta():
        model = User
        fields = ('first_name', 'email','password')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    def clean(self, *args, **kwargs):
        validation_error_msgs = {}

        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        email = self.cleaned_data.get('email')
        password =self.cleaned_data.get('password')
        nome = self.cleaned_data.get('first_name')

        email_bool = User.objects.filter(username=email).first()
        if not nome:
            validation_error_msgs['first_name'] = error_msg_required_field
        if not email:
            validation_error_msgs['email'] = error_msg_required_field
        if not password:
            validation_error_msgs['password'] = error_msg_required_field
        if email_bool:
            validation_error_msgs['email'] = error_msg_email_exists

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
class LoginForms(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    class Meta():
        model = User
        fields = ('username','password')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
    def clean(self, *args, **kwargs):
        validation_error_msgs = {}
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        email = self.cleaned_data.get('username')
        password_data =self.cleaned_data.get('password')

        usuario_db = User.objects.filter(username=email).first()


class PerfilForms(forms.ModelForm):
    class Meta:
        model = PerfilUser
        fields = ('cpf_cnpj','tipo')
        exclude = ('per_pessoa_fk',)

    def __init__(self, per_cod=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_cod = per_cod
