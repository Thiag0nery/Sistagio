from django.shortcuts import render
from django.views import View
from . import forms
from django.contrib.auth.models import User

class Home(View):
    templates_name = 'home/index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name)

class Login(View):
    templates_name = 'home/login.html'
    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name)

class Cadastro(View):
    templates_name = 'home/cadastro.html'
    def get(self, *args, **kwargs):
        self.campo = {
            'usuario': forms.UserForms(
                data=self.request.POST or None
            ),
        }
        self.usarioForm = self.campo['usuario']
        return render(self.request, self.templates_name, self.campo)

    def post(self, *args, **kwargs):

        pass