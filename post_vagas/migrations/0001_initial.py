# Generated by Django 4.2.6 on 2023-10-27 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostVagas',
            fields=[
                ('vag_cod', models.BigAutoField(primary_key=True, serialize=False)),
                ('vag_nome', models.CharField(blank=True, max_length=50, null=True)),
                ('vag_tell', models.CharField(blank=True, max_length=50, null=True)),
                ('vag_email', models.EmailField(blank=True, max_length=80, null=True)),
                ('vag_endereco', models.CharField(blank=True, max_length=40, null=True)),
                ('vag_descricao', models.TextField(blank=True, null=True)),
                ('vag_funcao', models.TextField(blank=True, null=True)),
                ('vag_beneficio', models.TextField(blank=True, max_length=100, null=True)),
                ('vag_usuario_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vaga_cadastradas',
            fields=[
                ('vcad_codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('vcad_perfil_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.perfiluser')),
                ('vcad_postVaga_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post_vagas.postvagas')),
            ],
        ),
    ]
