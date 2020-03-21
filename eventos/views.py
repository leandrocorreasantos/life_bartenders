from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'eventos/index.html')


def quem_somos(request):
    return render(request, 'eventos/quem_somos.html')


def agenda(request):
    return render(request, 'eventos/agenda.html')


def eventos(request):
    return render(request, 'eventos/eventos.html')


def evento(request):
    return render(request, 'eventos/evento.html')


def contato(request):
    return render(request, 'eventos/contato.html')
