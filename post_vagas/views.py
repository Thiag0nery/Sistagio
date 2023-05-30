from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from . import models
from django.db.models import Q

class ListaVagas(ListView):
    model = models.PostVagas
    template_name = 'post_vagas/vagas.html'
    context_object_name = 'vagas'

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
