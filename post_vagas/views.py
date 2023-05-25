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
class DetalheVaga(View):
    templates_name = 'post_vagas/vaga_detalhe.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        vag_cod = self.kwargs.get('vag_cod')
        post = get_object_or_404(models.PostVagas, vag_cod=vag_cod)

        self.conteudo = {
            'vaga':post
        }

        self.pagina = render(request, self.templates_name, self.conteudo)
    def get(self,request, *args, **kwargs):
        return render(self.request, self.templates_name, self.conteudo)