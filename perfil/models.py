from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from Sistagio import settings
class PerfilUser(models.Model):
    per_cod = models.BigAutoField(primary_key=True)
    per_nascimento = models.DateField(null=True,blank=True)
    per_pessoa_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')
    cpf_cnpj = models.CharField(max_length=15, blank=True)
    tipo = models.CharField(max_length=1, blank=True)

class Certificados(models.Model):
    cert_cod = models.BigAutoField(primary_key=True)
    cert_nome_curso = models.CharField(max_length=75)
    cert_instituicao = models.CharField(max_length=50)
    cert_arquivo = models.FileField(upload_to='certificados/%Y/%m/',null=True,blank=True)
    cert_pessoa_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')

class Aluno_Csv(models.Model):
    alu_codigo = models.BigAutoField(primary_key=True)
    alu_nome = models.CharField(max_length=50, null=True, verbose_name='Aluno')
    alu_matricula = models.CharField(max_length=20, null=True, verbose_name='Matricula')
    #alu_codigo = models.
    alu_turma = models.CharField(max_length=20, null=True, verbose_name='Turma')

    def __str__(self):
        return self.alu_nome,self.alu_turma

