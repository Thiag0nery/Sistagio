from django import forms
from . import models
from post_vagas.models import PostVagas
from django.contrib.auth.models import User
class PerfilForms(forms.ModelForm):


    class Meta:
        model = models.PerfilUser
        fields = '__all__'
        exclude = ('per_pessoa_fk',)



    def __init__(self, per_cod=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_cod = per_cod

class CertificadoForms(forms.ModelForm):
    class Meta:
        model = models.Certificados
        fields = '__all__'
        exclude = ('cert_pessoa_fk',)

class PostVagasForms(forms.ModelForm):
    class Meta:
        model = PostVagas
        fields = '__all__'
        exclude = ('vag_perfil_fk',)
class Tabela_csv(forms.ModelForm):
    class Meta:
        model = models.Aluno_Csv
        fields = '__all__'

class DocenteForm(forms.ModelForm):
    nome_docente = forms.CharField(
        widget=forms.TextInput
    )
    email_docente = forms.CharField(
        widget=forms.EmailInput
    )
    cpf_docente = forms.CharField(
        widget=forms.TextInput
    )
    senha_docente = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
    senha_docente2 = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    class Meta():
        model = User
        fields = ('nome_docente','email_docente','cpf_docente','cpf_docente','senha_docente2',)

    def clean(self, *args, **kwargs):
        validation_error_msgs = {}
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        email_docente = self.cleaned_data.get('email_docente')
        cpf_docente = self.cleaned_data.get('cpf_docente')
        nome_docente = self.cleaned_data.get('nome_docente')
        senha_docente = self.cleaned_data.get('senha_docente')
        senha_docente2 = self.cleaned_data.get('senha_docente2')

        email_bool = User.objects.filter(username=email_docente).first()

        # Verificação se o usuario preenceu todos os dados
        if not nome_docente:
            validation_error_msgs['nome_docente'] = error_msg_required_field
        if not email_docente:
            validation_error_msgs['email_docente'] = error_msg_required_field
        if not senha_docente:
            validation_error_msgs['senha_docente'] = error_msg_required_field
        if not senha_docente2:
            validation_error_msgs['senha_docente2'] = error_msg_required_field
        if not cpf_docente:
            validation_error_msgs['cpf_docente'] = error_msg_required_field

        # Verificação se existe email ja existente no sistema
        if email_bool:
            validation_error_msgs['email_docente'] = error_msg_email_exists

        # Verificação das senhas
        if senha_docente2 != senha_docente:
            validation_error_msgs['senha_docente'] = error_msg_password_match
            validation_error_msgs['senha_docente2'] = error_msg_password_match
        if len(senha_docente) < 6:
            validation_error_msgs['senha_docente'] = error_msg_password_short

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))
