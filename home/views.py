from django.shortcuts import render
from django.views import View

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
        return render(self.request, self.templates_name)