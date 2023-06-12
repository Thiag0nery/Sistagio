from typing import Any
from django import http
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from perfil.models import PerfilUser
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import models
from django.db.models import Q

class ListaVagas(View):
    template_name = 'post_vagas/vagas.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = PerfilUser.objects.filter(per_pessoa_fk=self.request.user).first()

        self.contexto = {
            'perfilUsuario':self.perfil
        }

        if self.perfil.tipo != 'E':
            self.contexto['vagas'] = models.PostVagas.objects.all()
        else:
            alunos_perfil = PerfilUser.objects.filter(tipo="A")
            self.contexto['alunos_perfil'] = alunos_perfil

        self.page = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.page
@csrf_exempt
def candidatos(request):
    id_post = request.POST.get('vaga_codigo')
    post_banco = models.PostVagas.objects.filter(vag_cod=int(id_post)).first()
    post_caditados = models.Vaga_cadastradas.objects.filter(vcad_postVaga_fk=post_banco)
    print(post_caditados)
    data = [{'nome':caditados.vcad_perfil_fk.per_pessoa_fk.first_name} for caditados in post_caditados]
    return JsonResponse({'data':data})

@csrf_exempt
def cadastro(request):
    perfil = PerfilUser.objects.filter(per_pessoa_fk=request.user).first()
    codigo_vaga = request.POST.get('vaga_codigo')

    vaga = models.PostVagas.objects.filter(vag_cod=int(codigo_vaga)).first()

    vaga_cadastrada = models.Vaga_cadastradas.objects.filter(
        vcad_perfil_fk=perfil, vcad_postVaga_fk=vaga).exists()
    if not vaga_cadastrada:
        models.Vaga_cadastradas(vcad_perfil_fk=perfil,vcad_postVaga_fk=vaga).save()

    data = {
        'certo':vaga_cadastrada
    }

    return JsonResponse(data)

@csrf_exempt
def vareficacao(request):
    perfil = PerfilUser.objects.filter(per_pessoa_fk=request.user).first()
    codigo_vaga = request.POST.get('vaga_codigo')
    print(codigo_vaga, 'aqui')
    vaga = models.PostVagas.objects.filter(vag_cod=int(codigo_vaga)).first()

    vaga_cadastrada = models.Vaga_cadastradas.objects.filter(
        vcad_perfil_fk=perfil,vcad_postVaga_fk=vaga).exists()
    data = {
        'certo':vaga_cadastrada
    }
    print(vaga_cadastrada)
    return JsonResponse(data)
class Busca(ListaVagas):
    model = models.PostVagas
    template_name = 'post_vagas/vagas.html'
    context_object_name = 'vagas'

    def get_queryset(self, *args, **kwargs):
        busca = self.request.GET.get('busca')
        qs = super().get_queryset(*args, **kwargs)
        if not busca:
            return qs
        qs = qs.filter(
            Q(vag_nome__icontains=busca)
        )
        return qs
