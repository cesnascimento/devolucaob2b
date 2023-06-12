from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('atualizar-devolucoes/', views.atualizar_devolucoes, name='atualizar-devolucoes'),

]