from django.urls import path
from  . import views

appname = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='inicial')
]