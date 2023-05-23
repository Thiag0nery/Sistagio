from django.db import models
from perfil.models import PerfilUser

class PostVagas(models.Model):
    vag_cod = models.BigAutoField(primary_key=True)
    vag_perfil_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE)
    vag_nome = models.CharField(max_length=50)
    vag_tell = models.CharField(max_length=50)
    vag_email = models.EmailField(max_length=80,null=True,blank=True)
    vag_endereco = models.CharField(max_length=20)
    vag_descricao = models.CharField(max_length=100)
    vag_funcao = models.CharField(max_length=50)
    vag_beneficio = models.CharField(max_length=100)
class Vaga_cadastradas(models.Model):
    vcad_codigo = models.BigAutoField(primary_key=True)
    vcad_perfil_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE)
    vcad_postVaga_fk = models.ForeignKey(PostVagas, on_delete=models.CASCADE)
