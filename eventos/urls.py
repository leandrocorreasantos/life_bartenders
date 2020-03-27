from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.urls import path  # reverse
from .models import Evento
from . import views

app_name = 'eventos'

infodict = {
    'queryset': Evento.eventos(),
    'date_field': 'data',
}


class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = "0.5"

    def items(self):
        return ['/quem-somos/', '/agenda/', '/eventos/', '/contato/']

    def location(self, item):
        return item


sitemaps = {
    'static': StaticSitemap,
    'eventos': GenericSitemap(infodict, priority=0.7, changefreq='weekly')
}

urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('agenda/', views.agenda, name='agenda'),
    path('eventos/', views.eventos, name='eventos'),
    path('evento/<slug>/<pk>/', views.evento, name='evento'),
    path('contato/', views.contato, name='contato'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path(
        'sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )

]
