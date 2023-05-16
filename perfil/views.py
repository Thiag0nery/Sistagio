from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from . import forms
from home.forms import UserForms
from django.contrib.auth.models import User
from . import models
from django.contrib import messages
import csv
import pandas as pd

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
            'perfilPessoa': self.perfil,
            'aluno_csv': forms.Tabela_csv(data=self.request.POST or None),
            'docente_formulario':forms.DocenteForm(data=self.request.POST or None)
        }

        self.usuarioForm = self.informacoes['usuario']
        self.usuarioPerfil = self.informacoes['perfil']
        self.certificado = self.informacoes['certificados']
        self.aluno = self.informacoes['aluno_csv']
        self.postvaga = self.informacoes['post']
        self.docenteFormulario = self.informacoes['docente_formulario']
    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name, self.informacoes)
class AtualizacaoPerfil(Perfil):


    def post(self, *args, **kwargs):
        botao_perfil = self.request.POST.get('botao-perfil')
        botao_certificado = self.request.POST.get('botao-certificado')
        botao_vag = self.request.POST.get('botao-vag')
        botao_csv = self.request.POST.get('botao-csv')

        usuario = get_object_or_404(
            User, username=self.request.user.username)
        """ PRECISSA REPARO - DATA  """
        if botao_perfil:
            if self.usuarioPerfil.is_valid():
                data = self.request.POST.get('per_nascimento')
                print(data)
                perfil = self.usuarioPerfil.save(commit=False)
                perfil.per_pessoa_fk = usuario
                perfil.per_nascimento = data
                perfil.save()

        if botao_certificado:
            print(bool(self.usuarioPerfil.is_valid()))
            """ PRECISSA REPARO - NULL NOS  CAMPOS"""
            documento = self.request.FILES.get('cert_arquivo')
            arquivo = self.certificado.save(commit=False)
            arquivo.cert_pessoa_fk = usuario
            arquivo.cert_arquivo = documento
            arquivo.save()
            print(documento,"a")
        if botao_vag:
            self.perfil = models.PerfilUser.objects.filter(
                per_pessoa_fk=self.request.user
            ).first()
            #pk_perfil = get_object_or_404(models.PerfilUser, per_pessoa_fk=self.request.user.username)
            print(self.perfil)
            post = self.postvaga.save(commit=False)
            post.vag_perfil_fk = self.perfil
            post.save()
        print(bool(botao_csv))

        if 'botao-csv' in self.request.POST:

            arquivo = self.request.FILES.get('arquivo')

            file = arquivo.read().decode('latin-1').splitlines()

            reader = csv.reader(file, delimiter=';')
            aluno_lista = []
            for linha,tabela in enumerate(reader):
                if linha <= 2:
                    continue
                nome = tabela[1]
                matricula = tabela[0]
                obj = models.Aluno_Csv(
                    alu_nome=nome,
                    alu_matricula=matricula,

                )
                models.Aluno_Csv.objects.filter(alu_nome=nome, alu_matricula=matricula).delete()

                aluno_lista.append(obj)

            models.Aluno_Csv.objects.bulk_create(aluno_lista)


        if 'btn-docente' in self.request.POST:


            if not self.docenteFormulario.is_valid():
                messages.error(
                    self.request,
                    self.docenteFormulario.errors
                )
                return redirect('perfil:perfil')
            nome_docente = self.request.POST.get('nome_docente')
            email_docente = self.request.POST.get('email_docente')
            senha_docente = self.request.POST.get('senha_docente')
            cpf_docente = self.request.POST.get('cpf_docente')


            docente = []
            objeto = User(
                username= email_docente,
                password=senha_docente,
                first_name = nome_docente,
                email= email_docente
            )
            docente.append(objeto)
            User.objects.bulk_create(docente)


            perfil = models.PerfilUser(
                per_pessoa_fk=objeto,
                tipo='D',
                cpf_cnpj= cpf_docente,

            )
            docente_perfil = []
            docente_perfil.append(perfil)
            models.PerfilUser.objects.bulk_create(docente_perfil)
        return redirect('home:inicial')



