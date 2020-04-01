# coding: utf-8
from django.shortcuts import render
from django.core.mail import BadHeaderError  # , send_mail
import smtplib
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ContatoForm
from .models import Evento, Galeria
from lifebartenders.settings import (
    CONTACT_EMAIL_BOX,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_SSL
)


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

            body_message = u"Nome: {}\nEmail: {}\nTelefone: {}\n\n{}".format(
                nome, email, telefone, msg
            )

            mensagem = u"\r\n".join((
                "From: %s" % EMAIL_HOST_USER,
                "To: %s" % CONTACT_EMAIL_BOX,
                "Subject: %s" % assunto,
                "Reply-To: %s" % email,
                "",
                body_message
            )).encode('utf-8')
            try:

                if EMAIL_USE_SSL is True:
                    smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
                    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                else:
                    smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                    smtp.use_ehlo_or_helo_if_needed()

                smtp.sendmail(EMAIL_HOST_USER, [CONTACT_EMAIL_BOX], mensagem)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "E-mail enviado com sucesso!"
                )
                print('email enviado')
                smtp.quit()
            except BadHeaderError as er:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Houve um erro ao enviar a mensagem"
                )
                print('cabeçalho com erro: {}'.format(er))
            except Exception as e:
                print(e)

    return render(request, 'eventos/contato.html', {'form': form})
