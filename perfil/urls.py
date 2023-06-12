from django.urls import path
from . import views
app_name = 'perfil'
urlpatterns = [
    path('', views.AtualizacaoPerfil.as_view(), name='perfil'),
    path('detalhe/<int:per_cod>/<int:curs_codigo>', views.perfilDetalheAluno.as_view(), name='detalhe'),
    path('detalhe/<int:per_cod>/', views.perfilDetalheAluno.as_view(), name='detalheperfil')
]