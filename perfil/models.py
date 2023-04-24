from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from Sistagio import settings
class PerfilUser(models.Model):
    per_cod = models.BigAutoField(primary_key=True)
    per_nascimento = models.DateField(null=True,blank=True)
    per_pessoa_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')
    cpf_cnpj = models.CharField(max_length=15, blank=True)
    tipo = models.CharField(max_length=1, blank=True, default='A', choices=(
        ('A', 'Aluno'),
        ('E', 'Empresa'),
        ('I', 'Instituição'),
        ('D', 'Docente'),
    ))

class Certificados(models.Model):
    cert_cod = models.BigAutoField(primary_key=True)
    cert_nome_curso = models.CharField(max_length=75)
    cert_instituicao = models.CharField(max_length=50)
    cert_arquivo = models.FileField(upload_to='certificados/%Y/%m/',null=True,blank=True)
    cert_pessoa_fk = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')