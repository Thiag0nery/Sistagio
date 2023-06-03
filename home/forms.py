from django import forms
from django.contrib.auth.models import User
from perfil.models import PerfilUser
from perfil.models import Aluno_Csv
class UserForms(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Senha',
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Confirma senha ',
    )

    class Meta():
        model = User
        fields = ('first_name', 'email','password','password2')

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
        password2 = self.cleaned_data.get('password2')
        nome = self.cleaned_data.get('first_name')



        email_bool = User.objects.filter(username=email).first()


        # Verificação se o usuario preenceu todos os dados
        if not nome:
            validation_error_msgs['first_name'] = error_msg_required_field
        if not email:
            validation_error_msgs['email'] = error_msg_required_field
        if not password:
            validation_error_msgs['password'] = error_msg_required_field
        if not password2:
            validation_error_msgs['password2'] = error_msg_required_field


        # Verificação se existe email ja existente no sistema
        if email_bool:
            validation_error_msgs['email'] = error_msg_email_exists

        # Verificação das senhas
        if password != password2:
            validation_error_msgs['password'] = error_msg_password_match
            validation_error_msgs['password2'] = error_msg_password_match
        if len(password) < 6:
            validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))


class PerfilForms(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('A', 'Aluno'),
            ('E', 'Empresa'),
            ('I', 'Instituição'),
        )

    )
    matricula = forms.CharField(
        max_length=14,
        required=False
    )

    class Meta:
        model = PerfilUser
        fields = ('cpf_cnpj', 'tipo_usuario','matricula')

    def __init__(self, per_cod=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_cod = per_cod

    def clean(self, *args, **kwargs):
        validation_error_msgs = {}

        #Mensagens de erro
        error_msg_cpf_cnpj_exists = 'Já existe no sistema'
        error_msg_not_matricula_exists = 'A matricula informada não existe no sistema'
        error_msg_required_field = 'Este campo é obrigatório.'

        tipo_usuario  = self.cleaned_data.get('tipo_usuario')
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        matricula =  self.cleaned_data.get('matricula')
        if matricula:
            matricula = matricula.replace('.','').replace(',','').replace('-','')
            matricula = int(matricula)

        cpf_cnpj_banco = PerfilUser.objects.filter(cpf_cnpj=cpf_cnpj).first()

        # Verificação se o usuario preenceu todos os dados
        if not cpf_cnpj:
            validation_error_msgs['cpf_cnpj'] = error_msg_required_field
        if tipo_usuario == "A":
            if not matricula:
                validation_error_msgs['matricula'] = error_msg_required_field

            # Verificação se o aluno existe no sistema
            matricula_banco = Aluno_Csv.objects.filter(alu_matricula=matricula).first()
            if not matricula_banco:
                validation_error_msgs['matricula'] = error_msg_not_matricula_exists

        # Verificação se existe cpf_cnpj ja existente no sistema
        if cpf_cnpj_banco:
            validation_error_msgs['cpf_cnpj'] = error_msg_cpf_cnpj_exists



        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))


class LoginForms(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    class Meta():
        model = User
        fields = ('username','password')


    def clean(self, *args, **kwargs):
        validation_error_msgs = {}
        validation_error_msgs['username'] = 'Usuario ou senha incoretos'
        raise (forms.ValidationError(validation_error_msgs))


