from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from . import forms
from django.contrib.auth import authenticate,login
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from . import models
from post_vagas.models import Vaga_cadastradas
from post_vagas.models import PostVagas
from django.contrib import messages
from perfil.models import Docente_curso
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core import serializers
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


        self.avaliacao = models.Avaliacao.objects.filter(ava_perfil_fk=self.perfil)
        self.avaliacao_verificado = models.Aluno_avaliado.objects.filter(alu_perfil_fk=self.perfil)

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
            'curso_oferecer': models.PerfilUser.objects.filter(tipo="I"),
            'docente_curso': self.docente_curso,
            'perfilPessoa': self.perfil,
            'alunos_inscritos':models.curso_aluno.objects.all(),
            'alunos_avaliados': list(models.Aluno_avaliado.objects.filter(alu_docente_fk=self.docente_perfil)),
            'curso_aluno_vinculado': self.curso_aluno,
            'vaga_cadastradas':self.vagaCadastradas,
            'aluno_csv': forms.Tabela_csv(data=self.request.POST or None),
            'docente_formulario':forms.DocenteForm(data=self.request.POST or None),
            'avaliacao': self.avaliacao,
            'aluno_verificado': self.avaliacao_verificado
        }
        if self.perfil.tipo == 'E':
            self.informacoes['vagas_lancadas'] = PostVagas.objects.filter(vag_usuario_fk=self.request.user)



        self.usuarioForm = self.informacoes['usuario']
        self.cursoform = self.informacoes['curso_instituicao']
        self.usuarioPerfil = self.informacoes['perfil']
        self.certificado = self.informacoes['certificados']
        self.aluno = self.informacoes['aluno_csv']
        self.postvaga = self.informacoes['post']
        self.docenteFormulario = self.informacoes['docente_formulario']
        # Saber a media do aluno
        if  self.perfil.tipo == "A":
            verificacao = models.Aluno_avaliado.objects.filter(alu_perfil_fk=self.perfil).exists()
            if verificacao:
                self.informacoes['lista_pergunta_media'] = media_aluno(self.avaliacao_verificado,self.avaliacao)

    def get(self, *args, **kwargs):

        return render(self.request, self.templates_name, self.informacoes)


def compactar_imagem(imagem, qualidade=80):
    # Abre a imagem usando o Pillow
    img = Image.open(imagem)

    # Cria um objeto BytesIO para armazenar a imagem compactada
    output = io.BytesIO()

    # Compacta a imagem com a qualidade desejada
    img.save(output, format='JPEG', quality=qualidade)

    # Retorna o conteúdo compactado da imagem
    return output.getvalue()
class AtualizacaoPerfil(Perfil):


    def post(self, *args, **kwargs):
        usuario = get_object_or_404(
            User, username=self.request.user.username)


        if 'mudar-foto' in self.request.POST:
            foto_pessoa =  self.request.FILES.get('perfil_foto_usuario')
            print(foto_pessoa)
            imagem_compactada = compactar_imagem(foto_pessoa)
            arquivo = SimpleUploadedFile('imagem.jpg', imagem_compactada)
            self.perfil.per_foto = arquivo
            self.perfil.save()
            return redirect('perfil:perfil')
        """ PRECISSA REPARO - DATA  """
        if 'dados-usuario' in self.request.POST:
            print('Entrou aqio')
            #password = self.usuarioForm.cleaned_data.get('password')


            first_name = self.usuarioForm.data.get('first_name')

            if not self.usuarioForm.is_valid():
                messages.error(
                    self.request,
                    self.usuarioForm.errors
                )
                return redirect('perfil:perfil')
            email = self.usuarioForm.data.get('email').lower()
            senha = self.usuarioForm.data.get('password')

            if email:
                usuario.email = email
                usuario.username = email
            if senha:
                usuario.set_password(senha)




            testa = self.usuarioPerfil.save()
            print(testa)



            if first_name:
                usuario.first_name = first_name
            usuario.save()
            if senha:
                return redirect('home:logout')

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
            print('a')
            nome_instituicao = self.request.POST.get('instituicao')
            nome_curso = self.request.POST.get('curso')
            if nome_curso:
                usuario = get_object_or_404(User, first_name=nome_instituicao)

                perfil = models.PerfilUser.objects.filter(per_pessoa_fk=usuario).first()

                curso_institui = get_object_or_404(models.curso_instituicao, curs_perfil_fk=perfil, curs_nome=nome_curso)
                aluno_curso = models.curso_aluno(curs_insituicao=curso_institui, curs_perfil_fk=self.perfil)
                aluno_curso.save()

            return redirect('perfil:perfil')

        return redirect('home:inicial')
class atualizarPerfil(Perfil):

    pass
class perfilDetalheAluno(View):
    templates_name = 'perfil/perfil_detalhe.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.perfil = models.PerfilUser.objects.filter(
            per_pessoa_fk=self.request.user
        ).first()
        primary_key = self.kwargs.get('per_cod')

        self.user_filter = User.objects.filter(id=int(primary_key)).first()

        self.perfil_filter = models.PerfilUser.objects.filter(per_pessoa_fk=self.user_filter).first()
        self.curso_aluno = models.curso_aluno.objects.filter(curs_perfil_fk=self.perfil_filter)
        self.contexto = {
            'perfil': self.perfil_filter,
            'perfil_visitante': self.perfil,
            'usuario': self.user_filter,
            'curso_aluno_vinculado': self.curso_aluno,
            'cursos_vinculados': models.curso_instituicao.objects.filter(curs_perfil_fk=self.perfil_filter),
            'certificados':models.Certificados.objects.filter(cert_pessoa_fk=self.perfil_filter)
        }
        if self.perfil.tipo == 'D':
            curso_codigo = self.kwargs.get('curs_codigo')
            self.docente_perfil = models.Docente.objects.filter(doce_perfil_pk=self.perfil).first()
            self.curso_selecionado = models.curso_aluno.objects.filter(
                curs_codigo=int(curso_codigo)).first()
            print(self.curso_selecionado.curs_codigo)
            verificacao_avaliado = models.Aluno_avaliado.objects.filter(
                alu_docente_fk=self.docente_perfil, alu_perfil_fk=self.perfil_filter
                ,alu_curso_aluno_fk=self.curso_selecionado).exists()
            self.contexto['perguntas'] = models.Perguntas.objects.all()
            self.contexto['verificao'] = verificacao_avaliado
        else:
            avaliacao_verificado = models.Aluno_avaliado.objects.filter(
                alu_perfil_fk=self.perfil_filter)
            avaliacao = models.Avaliacao.objects.filter(ava_perfil_fk=self.perfil_filter)
            self.contexto['avaliacao_verificado'] = models.Aluno_avaliado.objects.filter(
                alu_perfil_fk=self.perfil_filter)
            verificacao = models.Aluno_avaliado.objects.filter(alu_perfil_fk=self.perfil_filter).exists()
            print(verificacao)
            if verificacao:

                self.contexto['lista_pergunta_media'] = media_aluno(avaliacao_verificado, avaliacao)
        self.page = render(self.request, self.templates_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.page

    def post(self, *args, **kwargs):
        if 'curso_avaliacao' in self.request.POST:
            avaliacao = self.request.POST.getlist('valor_aluno')
            id_pergunta = self.request.POST.getlist('pergunta_id')
            list_object = []
            print(avaliacao)
            for numero,valor in enumerate(avaliacao):
                pergunta = get_object_or_404(models.Perguntas, per_codigo=int(id_pergunta[numero]))
                avaliacao_object = models.Avaliacao(
                    ava_docente_fk=self.docente_perfil,
                    ava_perfil_fk=self.perfil_filter,
                    ava_curso_aluno_fk=self.curso_selecionado,
                    ava_pergunta_fk=pergunta,
                    ava_nota=int(valor)
                )
                list_object.append(avaliacao_object)

            models.Avaliacao.objects.bulk_create(list_object)
            models.Aluno_avaliado(alu_docente_fk=self.docente_perfil,alu_perfil_fk=self.perfil_filter
                                  ,alu_curso_aluno_fk=self.curso_selecionado).save()


            return redirect('perfil:perfil')

def media_aluno(avaliacao_verificado,avaliacao):
    pergunta = models.Perguntas.objects.all()
    contador = []
    docentes_soma = 0
    for ava in avaliacao_verificado:
        docentes_soma += 1
        lista = []
        soma = 0
        for avalicao in avaliacao:
            if ava.alu_docente_fk == avalicao.ava_docente_fk \
                    and ava.alu_curso_aluno_fk.curs_insituicao.curs_nome == \
                    avalicao.ava_curso_aluno_fk.curs_insituicao.curs_nome:
                lista.append(avalicao.ava_nota)
                soma += avalicao.ava_nota
        contador.append(lista)
    #print(contador)
    media_perguntas = None
    for numero, soma_lista in enumerate(contador):
        if numero > 0:
            #print(media_perguntas, 'aqui')
            for numero, lista in enumerate(media_perguntas):
                media_perguntas[numero] += soma_lista[numero]
        else:
            media_perguntas = soma_lista
    #print(media_perguntas)
    #print(docentes_soma)
    for numero, lista in enumerate(media_perguntas):
        #print(lista)
        media_perguntas[numero] = lista / docentes_soma
    #print(media_perguntas)
    lista_pergunta_media = []
    for numero, pergunta in enumerate(pergunta):
        lista_pergunta_media.append((pergunta.per_pergunta, media_perguntas[numero]))

    return lista_pergunta_media

# Reciqurimento ajax
