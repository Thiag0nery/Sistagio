from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views import View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from perfil.forms import PerfilForms
from perfil.models import PerfilUser
class Home(View):
    templates_name = 'home/index.html'

    def get(self, *args, **kwargs):
        pagina = {}
        if self.request.user.is_authenticated:
            self.perfil = get_object_or_404(PerfilUser, per_pessoa_fk=self.request.user)
            pagina['perfilPessoa'] = self.perfil

        return render(self.request, self.templates_name, pagina)

class Login(View):
    templates_name = 'home/login.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.campo = {
            'usuario': forms.LoginForms(
                data=self.request.POST or None
            ),

        }
        self.usuarioForm = self.campo['usuario']
        self.pagina = render(self.request, self.templates_name, self.campo)

    def get(self, *args, **kwargs):
        return self.pagina

    # Pegara a requisição post vindo do formulario
    def post(self, *args, **kwargs):
        #Email que o usuario digitou
        email = self.request.POST.get('username')

        # Senha que o usuario digitou
        senha = self.request.POST.get('password')

        # Verificação se o usuario todos os campos
        if not email or not senha:

            return redirect('home:login')

        #Autentica o usuario, se achar o usuario no sistema a variavel usuario vai receber True se não achar vai ser
        #False

        usuario = authenticate(
            self.request, username=email, password=senha)

        if not usuario:
            messages.error(
                self.request,
                "Usuario ou senha incoretos!"
            )
            return redirect('home:login')

        login(self.request, user=usuario)

        return redirect('home:inicial')


class Cadastro(View):
    templates_name = 'home/cadastro.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.campo = {
            'usuario': forms.UserForms(
                data=self.request.POST or None
            ),
            'perfil': forms.PerfilForms(
                data=self.request.POST or None,
            )
        }
        self.usuarioForm = self.campo['usuario']
        self.perfilUser = self.campo['perfil']
        self.pagina = render(self.request, self.templates_name, self.campo)
    def get(self, *args, **kwargs):
        return self.pagina

    def post(self, *args, **kwargs):

        # Email que o usuario digitou
        email_requisicao = self.request.POST.get('email')

        # O Tipo de Usuario escolheu
        tipo_requisicao = self.request.POST.get('tipo_usuario')
        
        # A matricula que o usuario digitou
        matricula = self.request.POST.get('tipo_usuario')

        if not self.usuarioForm.is_valid():
            messages.error(
                self.request,
                self.usuarioForm.errors
            )
            return self.pagina
        if not self.perfilUser.is_valid():
            messages.error(
                self.request,
                self.perfilUser.errors
            )
            return self.pagina
        senha = self.usuarioForm.cleaned_data.get('password')
        usuario = self.usuarioForm.save(commit=False)
        usuario.username = email_requisicao
        if matricula == "I":
            usuario.is_active = False
        usuario.set_password(senha)
        usuario.save()

        perfil = self.perfilUser.save(commit=False)
        perfil.per_pessoa_fk = usuario
        perfil.tipo = tipo_requisicao
        perfil.save()

        if matricula == "I":
            messages.success(
                self.request,
                "Cadastro feito com sucesso, aguarde o periodo de verifição do sistema se a instituição e validada"
            )
            return redirect('home:inicial')
        """if senha:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=senha
            )

            if autentica:
                login(self.request, user=usuario)"""

        return redirect('home:login')

