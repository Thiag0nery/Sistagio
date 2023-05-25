from django.urls import path
from . import views
app_name = 'perfil'
urlpatterns = [
    path('load_second_options/', views.load_second_options.as_view(), name='load_second_options'),
    path('', views.AtualizacaoPerfil.as_view(), name='perfil'),
]