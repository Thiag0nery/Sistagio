from django.urls import path
from . import views
app_name = 'post_vagas'
urlpatterns = [
    path('',views.ListaVagas.as_view(),name='homepage'),
    path('vagadetalhe/<int:vag_cod>', views.DetalheVaga.as_view(), name='detalhe'),
]