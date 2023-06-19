from django.db import models
from perfil.models import PerfilUser
from django.contrib.auth.models import User

class PostVagas(models.Model):
    vag_cod = models.BigAutoField(primary_key=True)
    vag_usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    vag_nome = models.CharField(max_length=50,null=True,blank=True)
    vag_tell = models.CharField(max_length=50,null=True,blank=True)
    vag_email = models.EmailField(max_length=80,null=True,blank=True)
    vag_endereco = models.CharField(max_length=40,null=True,blank=True)
    vag_descricao = models.TextField(null=True,blank=True)
    vag_funcao = models.TextField(null=True,blank=True)
    vag_beneficio = models.TextField(max_length=100,null=True,blank=True)

    def __repr__(self):
        return self.vag_nome
class Vaga_cadastradas(models.Model):
    vcad_codigo = models.BigAutoField(primary_key=True)
    vcad_perfil_fk = models.ForeignKey(PerfilUser, on_delete=models.CASCADE)
    vcad_postVaga_fk = models.ForeignKey(PostVagas, on_delete=models.CASCADE)

