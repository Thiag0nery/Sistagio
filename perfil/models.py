from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from Sistagio import settings
class PerfilUser(models.Model):
    per_cod = models.BigAutoField(primary_key=True)
    per_nascimento = models.DateField(null=True,blank=True)
    per_pessoa_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')
    cpf_cnpj = models.CharField(max_length=18, blank=True)
    per_tell = models.CharField(max_length=14, blank=True)
    tipo = models.CharField(max_length=1, blank=True)
    per_foto = models.FileField(upload_to='fotos_usuario/%Y/%m/', null=True, blank=True)
    per_detalhe = models.CharField(max_length=255, blank=True )


class Certificados(models.Model):
    cert_cod = models.BigAutoField(primary_key=True)
    cert_nome_curso = models.CharField(max_length=75)
    cert_instituicao = models.CharField(max_length=50)
    cert_arquivo = models.FileField(upload_to='certificados/%Y/%m/',null=True,blank=True)
    cert_pessoa_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE,verbose_name='Usuario')

class Aluno_Csv(models.Model):
    alu_codigo = models.BigAutoField(primary_key=True)
    alu_nome = models.CharField(max_length=50, null=True, verbose_name='Aluno')
    alu_matricula = models.CharField(max_length=20, null=True, verbose_name='Matricula')
    #alu_codigo = models.
    alu_turma = models.CharField(max_length=20, null=True, verbose_name='Turma')
    alu_vinculado = models.BooleanField(default=False)
    def __str__(self):
        return self.alu_nome
class curso_instituicao(models.Model):
    curs_codigo  = models.BigAutoField(primary_key=True)
    curs_nome = models.CharField(max_length=45, null=True)
    curs_perfil_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE)

class curso_aluno(models.Model):
    curs_codigo  = models.BigAutoField(primary_key=True)
    curs_insituicao = models.ForeignKey(curso_instituicao, on_delete=models.CASCADE)
    curs_perfil_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE)

class Docente(models.Model):
    doce_codigo = models.BigAutoField(primary_key=True)
    doce_perfil_pk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE, null=True)
    doce_instituicao_fk = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
class Docente_curso(models.Model):
    doce_codigo  = models.BigAutoField(primary_key=True)
    doce_docente_pk = models.ForeignKey(Docente, on_delete=models.CASCADE,null=True)
    doce_curso_instituicao_fk = models.ForeignKey(curso_instituicao, on_delete=models.CASCADE, null=True)
class Perguntas(models.Model):
    per_codigo = models.BigAutoField(primary_key=True)
    per_pergunta = models.CharField(max_length=155, null=True, blank=True)
