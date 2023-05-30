from django.urls import path
from . import views
app_name = 'post_vagas'
urlpatterns = [
    path('',views.ListaVagas.as_view(),name='homepage'),
    path('busca/', views.Busca.as_view(), name='busca')
]