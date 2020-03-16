from django.db import models
import os
import glob
from slugify import slugify

# Create your models here.


class Estado(models.Model):
    nome = models.CharField('Nome', max_length=100)
    uf = models.CharField('UF', max_length=2)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    nome = models.CharField('Nome', max_length=100)
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        verbose_name='Estado'
    )

    def __str__(self):
        return '%s - %s' % (self.nome, self.estado.uf)


class Evento(models.Model):
    titulo = models.CharField('Título', max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    descricao = models.TextField('Descrição')
    data = models.DateTimeField('Data do Evento')
    local = models.CharField('Local do Evento', max_length=255)
    visivel = models.BooleanField('Visível', default=True)
    capa = models.ImageField(
        'Capa', upload_to='eventos/capa/', blank=True, null=True
    )
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.titulo

    def save(self):
        # set slug:
        new_slug = u"%s %s" % (
            self.titulo,
            self.data.strftime('%d %m %Y')
        )
        self.slug = slugify(new_slug)

        if self.pk:
            this = Evento.objects.get(pk=self.pk)
            try:
                if this.capa != self.capa:
                    path = "%s*" % (this.capa.path)
                    for arq in glob.glob(path):
                        os.remove(arq)
            except:
                pass

        super(Evento, self).save()

    def delete(self):
        try:
            self.capa.delete(save=False)
        except:
            pass
        super(Evento, self).delete()


class Galeria(models.Model):
    imagem = models.ImageField(upload_to='eventos/galeria/')
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.imagem)

    def save(self):
        if self.pk:
            this = Galeria.objects.get(pk=self.pk)

            # update image
            try:
                if this.imagem != self.imagem:
                    path = "%s*" % (this.imagem.path)
                    for arq in glob.glob(path):
                        os.remove(arq)
            except:
                pass

        super(Galeria, self).save()

    def delete(self):
        try:
            self.imagem.delete(save=False)
        except:
            pass
        super(Galeria, self).delete()
