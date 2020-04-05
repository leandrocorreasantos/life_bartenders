# coding: utf-8
from django import forms


class ContatoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            placeholder = '{}'
            if visible.field.required:
                placeholder = '{} *'
            visible.field.widget.attrs['placeholder'] = placeholder.format(
                visible.name.title()
            )

    nome = forms.CharField(required=True)
    telefone = forms.CharField()
    email = forms.EmailField(required=True)
    mensagem = forms.CharField(widget=forms.Textarea, required=True)
