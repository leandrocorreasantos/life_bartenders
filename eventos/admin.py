from django.contrib import admin

# Register your models here.

from .models import Estado, Cidade, Evento, Galeria


class GaleriaInline(admin.TabularInline):
    model = Galeria
    fields = ['imagem', ]
    verbose_name = 'Imagens'


class EventoAdmin(admin.ModelAdmin):
    exclude = ['slug']
    search_fields = ['titulo', 'local']
    inlines = [GaleriaInline, ]

# custom admin variables
admin.site.site_header = 'Life Bartenders'
admin.site.site_title = 'Life Bartenders'
admin.site.site_url = 'http://lifebartenders.com.br'
admin.site.index_title = 'Painel Administrativo'
# add admin panels
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Evento, EventoAdmin)
