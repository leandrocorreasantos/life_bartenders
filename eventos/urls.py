from django.urls import path  # , re_path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('agenda/', views.agenda, name='agenda'),
    path('eventos/', views.eventos, name='eventos'),
    path('evento/<slug>/<pk>/', views.evento, name='evento'),
    path('contato/', views.contato, name='contato')
]
