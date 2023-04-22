from django import forms
from . import models

class PerfilForms(forms.ModelForm):
    class Meta:
        model = models.PerfilUser
        fields = '__all__'
        exclude = ('per_pessoa_fk',)

    def __init__(self, per_cod=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_cod = per_cod

