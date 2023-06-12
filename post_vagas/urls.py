from django.urls import path
from . import views
app_name = 'post_vagas'
urlpatterns = [
    path('',views.ListaVagas.as_view(),name='homepage'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('verificacao/', views.vareficacao, name='verificacao'),
    path('candidatos/', views.candidatos, name='candidatos'),
    path('busca/', views.Busca.as_view(), name='busca')
]