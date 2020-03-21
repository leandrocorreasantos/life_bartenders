from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('agenda/', views.agenda, name='agenda'),
    path('eventos/', views.eventos, name='eventos'),
    path('evento/<slug:slug>/<int:pk>/', views.evento, name='evento'),
    path('contato/', views.contato, name='contato')
]
