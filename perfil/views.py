from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from . import forms
from django.contrib.auth.models import User
from . import models
from post_vagas.models import Vaga_cadastradas
from django.contrib import messages
from perfil.models import Docente_curso
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
import csv


class Perfil(View):
    templates_name = 'perfil/perfil.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        # Essa variavel permite pega o perfil do usuario no banco
        self.perfil = models.PerfilUser.objects.filter(
            per_pessoa_fk=self.request.user
        ).first()




        # Essa variavel permite pegar as vagas que o aluno se inscreveu
        self.vagaCadastradas = Vaga_cadastradas.objects.filter(vcad_perfil_fk=self.perfil)
        self.cursoVinculado = models.curso_instituicao.objects.filter(curs_perfil_fk=self.perfil)
        self.certificado = models.Certificados.objects.filter(cert_pessoa_fk=self.perfil)
        self.docenteVinculados = models.Docente.objects.filter(doce_instituicao_fk=self.request.user)
        self.docente_perfil = models.Docente.objects.filter(doce_perfil_pk=self.perfil).first()
        self.docente_curso = Docente_curso.objects.filter(doce_docente_pk=self.docente_perfil)
        self.curso_aluno = models.curso_aluno.objects.filter(curs_perfil_fk=self.perfil)


        self.informacoes = {
            'perfil': forms.PerfilForms(
                data=self.request.POST or None,
                instance=self.perfil
            ),
            'usuario': forms.UsuarioAtualizar(
                data=self.request.POST or None,
                usuario=self.request.user,
                instance=self.request.user
            ),
            'certificados': forms.CertificadoForms(
                data=self.request.POST or None
            ),
            'certificados_usuario':self.certificado,
            'post': forms.PostVagasForms(
                data=self.request.POST or None
            ),
            'curso_instituicao':forms.Curso_instituicao(data=self.request.POST or None),
            'curso_vinculado': self.cursoVinculado,
            'docente_vinculado': self.docenteVinculados,
            'curso_oferecer':models.curso_instituicao.objects.all(),
            'docente_curso': self.docente_curso,
            'perfilPessoa': self.perfil,
            'alunos_inscritos':models.curso_aluno.objects.all(),
            'alunos_avaliados': models.Aluno_avaliado.objects.filter(alu_docente_fk=self.docente_perfil),
            'curso_aluno_vinculado': self.curso_aluno,
            'vaga_cadastradas':self.vagaCadastradas,
            'aluno_csv': forms.Tabela_csv(data=self.request.POST or None),
            'docente_formulario':forms.DocenteForm(data=self.request.POST or None)
        }
        print(json.dumps(list(models.curso_aluno.objects.all().values()), cls=DjangoJSONEncoder))


        self.usuarioForm = self.informacoes['usuario']
        self.cursoform = self.informacoes['curso_instituicao']
        self.usuarioPerfil = self.informacoes['perfil']
        self.certificado = self.informacoes['certificados']
        self.aluno = self.informacoes['aluno_csv']
        self.postvaga = self.informacoes['post']
        self.docenteFormulario = self.informacoes['docente_formulario']
    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name, self.informacoes)
class AtualizacaoPerfil(Perfil):


    def post(self, *args, **kwargs):
        usuario = get_object_or_404(
            User, username=self.request.user.username)


        if 'mudar-foto' in self.request.POST:
            foto_pessoa =  self.request.FILES.get('perfil_foto_usuario')

            self.perfil.per_foto = foto_pessoa
            self.perfil.save()
            return redirect('perfil:perfil')
        """ PRECISSA REPARO - DATA  """
        if 'dados-usuario' in self.request.POST:
            print('Entrou')
            #password = self.usuarioForm.cleaned_data.get('password')
            #email = self.usuarioForm.data.get('email')
            first_name = self.usuarioForm.data.get('first_name')
            if self.usuarioPerfil.is_valid():

                perfilUsuario = self.usuarioPerfil.save(commit=False)
                perfilUsuario.per_pessoa_pk = usuario
                perfilUsuario.save()

            if first_name:
                usuario.first_name = first_name
            usuario.save()
            return redirect('perfil:perfil')

        if 'botao-certificado' in self.request.POST:
            documento = self.request.FILES.get('cert_arquivo')
            arquivo = self.certificado.save(commit=False)
            arquivo.cert_pessoa_fk = self.perfil
            arquivo.cert_arquivo = documento
            arquivo.save()
            return redirect('perfil:perfil')
        if 'botao-vag'  in self.request.POST:
            post = self.postvaga.save(commit=False)
            post.vag_usuario_fk =  usuario
            post.save()

            objeto = Vaga_cadastradas(
                vcad_perfil_fk=self.perfil,
                vcad_postVaga_fk=post
            )
            objeto.save()

            return redirect('perfil:perfil')

        if 'botao-csv' in self.request.POST:

            arquivo = self.request.FILES.get('arquivo')
            #arquivo_curso = self.request.FILES.get('arquivo_curso') or not arquivo_curso
            arquivo_nome_turma = self.request.POST.get('arquivo_nome_turma')

            if not arquivo or not arquivo_nome_turma:
                messages.error(
                    self.request,
                    "Digite todos os campos para o envio"
                )
                return redirect('perfil:perfil')

            file = arquivo.read().decode('latin-1').splitlines()

            reader = csv.reader(file, delimiter=';')
            aluno_lista = []
            for linha,tabela in enumerate(reader):
                if linha <= 2:
                    continue
                nome = tabela[1]

                matricula = tabela[0].replace('.','').replace(',','').replace('-','')
                obj = models.Aluno_Csv(
                    alu_nome=nome,
                    alu_matricula=matricula,
                    alu_turma=arquivo_nome_turma,

                )
                models.Aluno_Csv.objects.filter(alu_nome=nome, alu_matricula=matricula
                                                ,alu_turma=arquivo_nome_turma).delete()

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


            docente = User(
                username= email_docente.lower(),
                first_name = nome_docente,
                email= email_docente
            )
            docente.set_password(senha_docente)
            docente.save()


            perfil = models.PerfilUser(
                per_pessoa_fk=docente,
                tipo='D',
                cpf_cnpj= cpf_docente,

            )
            docente_perfil = []
            docente_perfil.append(perfil)
            models.PerfilUser.objects.bulk_create(docente_perfil)

            instituicao_docente = models.Docente(doce_perfil_pk=perfil, doce_instituicao_fk=usuario)
            instituicao_docente.save()


            curso_docente = self.request.POST.getlist('curso_docente')

            for value in curso_docente:
                curso_instituicao = get_object_or_404(models.curso_instituicao, curs_codigo=int(value))

                docente_curso = Docente_curso(doce_docente_pk=instituicao_docente,
                                              doce_curso_instituicao_fk=curso_instituicao)
                docente_curso.save()


            return redirect('perfil:perfil')

        if 'botao-curso-instituicao' in self.request.POST:
            curso = self.cursoform.save(commit=False)
            curso.curs_perfil_fk = self.perfil
            curso.save()

        if 'curso_escolhido' in self.request.POST:
            nome_instituicao = self.request.POST.get('instituicao')
            nome_curso = self.request.POST.get('curso')
            usuario = get_object_or_404(User, first_name=nome_instituicao)

            perfil = models.PerfilUser.objects.filter(per_pessoa_fk=usuario).first()

            curso_institui = get_object_or_404(models.curso_instituicao, curs_perfil_fk=perfil, curs_nome=nome_curso)

            print(curso_institui, 'Aqui')
            aluno_curso = models.curso_aluno(curs_insituicao=curso_institui, curs_perfil_fk=self.perfil)
            aluno_curso.save()

            return redirect('perfil:perfil')

        return redirect('home:inicial')
class perfilDetalheAluno(View):
    def setup(self, *args, **kwargs):
        super().setup( *args, **kwargs)
        print(self.request.per_cod)

