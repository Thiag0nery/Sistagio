from django.contrib import admin
from . import models
class AlunoCsvAdmin(admin.ModelAdmin):
    list_display = ('alu_nome','alu_matricula','alu_turma',)
admin.site.register(models.PerfilUser)
admin.site.register(models.Certificados)
admin.site.register(models.Docente)
admin.site.register(models.Aluno_Csv, AlunoCsvAdmin)
admin.site.register(models.curso_instituicao)
admin.site.register(models.curso_aluno)
# Register your models here.
