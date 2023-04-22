from django.urls import path
from . import views
app_name = 'perfil'
urlpatterns = [
    path('', views.AtualizacaoPerfil.as_view(), name='perfil'),

]