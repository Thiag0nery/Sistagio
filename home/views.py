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

    def post(self, *args, **kwargs):

        email = self.request.POST.get('username')
        senha = self.request.POST.get('password')

        if not email or not senha:
            print('Erro 1')
            return redirect('home:login')
        usuario = authenticate(
            self.request, username=email, password=senha)

        if not usuario:
            print('Erro 2')
            return redirect('home:login')

        login(self.request, user=usuario)
        print('certo')
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
        email_requisicao = self.request.POST.get('email')
        tipo_requisicao = self.request.POST.get('tipo_usuario')
        """
            PRECISSA REPARO - DATA
        """
        if not self.usuarioForm.is_valid():

            return self.pagina
        senha = self.usuarioForm.cleaned_data.get('password')
        usuario = self.usuarioForm.save(commit=False)
        usuario.username = email_requisicao
        usuario.set_password(senha)
        usuario.save()

        perfil = self.perfilUser.save(commit=False)
        perfil.per_pessoa_fk = usuario
        perfil.tipo = tipo_requisicao
        perfil.save()


        if senha:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=senha
            )

            if autentica:
                login(self.request, user=usuario)

        return redirect('home:login')

