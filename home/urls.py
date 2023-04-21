from django.urls import path
from  . import views

app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='inicial'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('cadastro/', views.CadastrarUsuario.as_view(), name='cadastro'),
]