from django.urls import path
from  . import views

appname = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='inicial'),
    path('login/', views.Login.as_view(), name='login'),
    path('cadastro/', views.Cadastro.as_view(), name='cadastro'),
]