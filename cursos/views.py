from django.http import JsonResponse
from perfil.models import curso_instituicao
from perfil.models import PerfilUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def load_second_options(request):
    id = request.GET.get('curs_codigo')
    usuario = get_object_or_404(User, first_name=id)
    perfil = PerfilUser.objects.filter(per_pessoa_fk=usuario).first()
    produto = curso_instituicao.objects.filter(curs_perfil_fk=perfil)
    print(produto)
    opcao = [{'id': produs.curs_codigo, 'name':produs.curs_nome} for produs in produto]
    return JsonResponse({'options':opcao})


