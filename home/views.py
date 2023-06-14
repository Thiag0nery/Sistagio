from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views import View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from perfil.forms import PerfilForms
from perfil.models import curso_instituicao
from perfil.models import PerfilUser
from perfil.models import Aluno_Csv
from perfil.models import curso_aluno
from django.core.mail import send_mail

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
        email = self.request.POST.get('username').lower()

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
                self.usuarioForm.errors
            )
            return self.pagina

        login(self.request, user=usuario)

        return redirect('post_vagas:homepage')


class Cadastro(View):
    templates_name = 'home/cadastro.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.campo = {
            'usuario': forms.UserForms(
                data=self.request.POST or None
            ),
            'curso_oferecer': PerfilUser.objects.filter(tipo="I"),
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
        email_requisicao = self.request.POST.get('email').lower()
        print(email_requisicao)
        # O Tipo de Usuario escolheu
        tipo_requisicao = self.request.POST.get('tipo_usuario')

        # A matricula que o usuario digitou
        matricula = self.request.POST.get('matricula')


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
        if tipo_requisicao == "I":
            usuario.is_active = False
        usuario.set_password(senha)
        usuario.save()


        perfil = self.perfilUser.save(commit=False)
        perfil.per_pessoa_fk = usuario
        perfil.tipo = tipo_requisicao
        perfil.save()

        if tipo_requisicao == "I":
            messages.success(
                self.request,
                "Cadastro feito com sucesso, aguarde o periodo de verifição do sistema se a instituição e validada"
            )

            subject = 'Obrigado pela sua inscrição no sistema'
            message = 'Cadastro feito com sucesso, aguarde o periodo de verifição do sistema' \
                      ' se a instituição e validada.'
            from_email = 'sistagio@hotmail.com'
            recipient_list = [email_requisicao, ]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            subject = 'Cadastro de Instituição feita'
            message = f'A instituição {usuario.first_name} esta na fila de verificação.'
            from_email = 'sistagio@hotmail.com'
            recipient_list = ['sistagio@hotmail.com', ]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('home:inicial')




        if tipo_requisicao == "A":
            matricula = str(int(matricula.replace('.', '').replace(',', '').replace('-', '')))

            matricula_banco = Aluno_Csv.objects.filter(alu_matricula=matricula).first()
            matricula_banco.alu_vinculado = True
            matricula_banco.save()
            nome_instituicao = self.request.POST.get('instituicao')
            nome_curso = self.request.POST.get('curso')
            usuario_instituicao = get_object_or_404(User, first_name=nome_instituicao)

            perfil_instituicao = PerfilUser.objects.filter(per_pessoa_fk=usuario_instituicao).first()

            curso_institui = get_object_or_404(curso_instituicao,
                                               curs_perfil_fk=perfil_instituicao, curs_nome=nome_curso)

            aluno_curso = curso_aluno(curs_insituicao=curso_institui, curs_perfil_fk=perfil)
            aluno_curso.save()

        subject = 'Obrigado pela sua inscrição no sistema'
        message = 'Obrigado pela sua inscrição no sistema.'
        from_email = 'sistagio@hotmail.com'
        recipient_list = [email_requisicao, ]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('home:login')

class Logout(View):
    def get(self, *args,**kwargs):
        logout(self.request)
        return redirect('home:inicial')