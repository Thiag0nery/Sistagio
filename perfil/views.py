from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from . import forms
from home.forms import UserForms
from django.contrib.auth.models import User
from . import models
import csv
import io

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
            'aluno_csv': forms.Tabela_csv(data=self.request.POST or None)
        }

        self.usuarioForm = self.informacoes['usuario']
        self.usuarioPerfil = self.informacoes['perfil']
        self.certificado = self.informacoes['certificados']
        self.aluno = self.informacoes['aluno_csv']
        self.postvaga = self.informacoes['post']
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

        def save_data(data):
            aux = []
            for item in data:
                print(str(item.get('NOME')))
                nome_aluno = item.get(';;;;CURSO:;Técnico em Desenvolvimento de Sistemas;;;;;;;')
                numero_matricula = str(item.get('R.A.'))

                obj = models.Aluno_Csv(
                    alu_nome=nome_aluno,
                    alu_matricula=numero_matricula,


                )
                aux.append(obj)

            models.Aluno_Csv.objects.bulk_create(aux)

        arquivo = self.request.FILES.get('arquivo')

        file = arquivo.read().decode('ISO-8859-1')
        reader = csv.DictReader(io.StringIO(file))

        data = [line for line in reader]

        save_data(data)

        return redirect('home:inicial')
"""def csv_to_list(filename: str) -> list:
    '''
    Lê um csv e retorna um OrderedDict.
    Créditos para Rafael Henrique
    https://bit.ly/2FLDHsH
    '''
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_data = [line for line in reader]
    return csv_data


def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        nome_aluno = item.get('NOME')
        numero_matricula = str(item.get('R.A.'))
        turma = item.get('G79980')
        obj = models.Aluno_Csv(
            alu_nome=nome_aluno,
            alu_matricula=numero_matricula,
            alu_turma=turma,

        )
        aux.append(obj)
    models.Aluno_Csv.objects.bulk_create(aux)


data = csv_to_list('fix/produtos.csv')
save_data(data)"""

