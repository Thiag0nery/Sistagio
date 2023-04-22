from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import View
from . import forms
from django.contrib.auth.models import User

class Home(View):
    templates_name = 'home/index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name)

class Login(View):
    templates_name = 'home/login.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.campo = {
            'usuario': forms.UserForms(
                data=self.request.POST or None
            ),
        }
        self.usuarioForm = self.campo['usuario']
        self.pagina = render(self.request, self.templates_name, self.campo)

    def get(self, *args, **kwargs):
        return self.pagina


class LoginUser(Login):
    def post(self, *args,**kwargs):
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

        }
        self.usuarioForm = self.campo['usuario']
        self.pagina = render(self.request, self.templates_name, self.campo)
    def get(self, *args, **kwargs):
        return self.pagina

class CadastrarUsuario(Cadastro):
    def post(self, *args, **kwargs):
        senha = self.usuarioForm.cleaned_data.get('password')

        usuario = self.usuarioForm.save(commit=False)
        usuario.set_password(senha)
        usuario.save()
        if senha:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=senha
            )

            if autentica:
                login(self.request, user=usuario)

        return redirect('home:login')

