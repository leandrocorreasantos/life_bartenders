from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ContatoForm
from .models import Evento, Galeria
from lifebartenders.settings import CONTACT_EMAIL_BOX


# Create your views here.
def index(request):
    proximo = Evento.proximo()
    agendas = Evento.agenda()[:4]
    eventos = Evento.eventos()[:4]
    return render(
        request,
        'eventos/index.html',
        {
            'proximo': proximo,
            'agendas': agendas,
            'eventos': eventos
        }
    )


def quem_somos(request):
    return render(request, 'eventos/quem_somos.html')


def agenda(request):
    page = request.GET.get('page', 1)
    next_event = Evento.proximo()
    agendas_search = Evento.agenda()
    paginator = Paginator(agendas_search, 12)
    agendas = paginator.get_page(page)
    return render(
        request,
        'eventos/agenda.html',
        {
            'next_event': next_event,
            'agendas': agendas
        }
    )


def eventos(request):
    page = request.GET.get('page', 1)
    eventos_search = Evento.eventos()
    paginator = Paginator(eventos_search, 12)
    eventos = paginator.get_page(page)
    return render(request, 'eventos/eventos.html', {'eventos': eventos})


def evento(request, slug, pk):
    page = request.GET.get('page', 1)
    evento = Evento.objects.get(pk=pk)
    galeria_search = Galeria.objects.filter(evento_id=pk).all()
    paginator = Paginator(galeria_search, 8)
    galeria = paginator.get_page(page)
    return render(
        request,
        'eventos/evento.html',
        {
            'evento': evento,
            'galeria': galeria
        }
    )


def contato(request):
    assunto = 'Life Bartenders - Contato do Site'
    form = ContatoForm()
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            msg = form.cleaned_data['mensagem']
            mensagem = "Nome: {}\nEmail: {}\nTelefone: {}\n\n{}".format(
                nome, email, telefone, msg
            )
            try:
                send_mail(assunto, mensagem, email, [CONTACT_EMAIL_BOX])
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "E-mail enviado com sucesso!"
                )
                print('email enviado')
            except BadHeaderError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Houve um erro ao enviar a mensagem"
                )
                print('cabeçalho com erro')
            except Exception as e:
                print(e)

    return render(request, 'eventos/contato.html', {'form': form})
