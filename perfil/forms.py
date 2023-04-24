from django import forms
from . import models
from post_vagas.models import PostVagas
class PerfilForms(forms.ModelForm):
    class Meta:
        model = models.PerfilUser
        fields = '__all__'
        exclude = ('per_pessoa_fk',)

    def __init__(self, per_cod=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.per_cod = per_cod

class CertificadoForms(forms.ModelForm):
    class Meta:
        model = models.Certificados
        fields = '__all__'
        exclude = ('cert_pessoa_fk',)

class PostVagasForms(forms.ModelForm):
    class Meta:
        model = PostVagas
        fields = '__all__'
        exclude = ('vag_perfil_fk',)
