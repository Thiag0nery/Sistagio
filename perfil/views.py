from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from . import forms
from home.forms import UserForms
from django.contrib.auth.models import User
from . import models

class Perfil(View):
    templates_name = 'perfil/perfil.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.perfil = models.PerfilUser.objects.filter(
            per_pessoa_fk=self.request.user
        ).first()
        self.informacoes = {
            'perfil': forms.PerfilForms(
                data=self.request.POST or None,
                per_cod=self.request.user,
                instance=self.perfil
            ),
            'usuario': UserForms(
                data=self.request.POST or None

            ),
            'certificados': forms.CertificadoForms(
                data=self.request.POST or None
            ),
            'post': forms.PostVagasForms(
                data=self.request.POST or None
            ),
        }

        self.usuarioForm = self.informacoes['usuario']
        self.usuarioPerfil = self.informacoes['perfil']
        self.certificado = self.informacoes['certificados']
        self.postvaga = self.informacoes['post']
    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name, self.informacoes)
class AtualizacaoPerfil(Perfil):

    def post(self, *args, **kwargs):
        usuario = get_object_or_404(
            User, username=self.request.user.username)
        """ PRECISSA REPARO - DATA 
        if self.usuarioPerfil.is_valid():
            data = self.request.POST.get('per_nascimento')
            print(data)
            perfil = self.usuarioPerfil.save(commit=False)
            perfil.per_pessoa_fk = usuario
            perfil.per_nascimento = data
            perfil.save()
        """
        print(bool(self.usuarioPerfil.is_valid()))
        """ PRECISSA REPARO - NULL NOS  CAMPOS
        documento = self.request.FILES.get('cert_arquivo')
        arquivo = self.certificado.save(commit=False)
        arquivo.cert_pessoa_fk = usuario
        arquivo.cert_arquivo = documento
        arquivo.save()
        print(documento,"a")
        """
        self.perfil = models.PerfilUser.objects.filter(
            per_pessoa_fk=self.request.user
        ).first()
        #pk_perfil = get_object_or_404(models.PerfilUser, per_pessoa_fk=self.request.user.username)
        print(self.perfil)
        post = self.postvaga.save(commit=False)
        post.vag_perfil_fk = self.perfil
        post.save()

        return redirect('home:inicial')

