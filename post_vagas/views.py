from typing import Any
from django import http
from django.shortcuts import render,get_object_or_404
from django.views import View
from perfil.models import PerfilUser
from django.views.generic.list import ListView
from . import models
from django.db.models import Q

class ListaVagas(View):
    template_name = 'post_vagas/vagas.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = PerfilUser.objects.filter(per_pessoa_fk=self.request.user).first()

        self.contexto = {
            'vagas': models.PostVagas.objects.all(),
            'perfilUsuario':self.perfil
        }

        self.page = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.page



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
