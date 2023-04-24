# Generated by Django 4.2 on 2023-04-23 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfil', '0004_alter_perfiluser_per_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiluser',
            name='per_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Certificados',
            fields=[
                ('cert_cod', models.BigAutoField(primary_key=True, serialize=False)),
                ('cert_nome_curso', models.CharField(max_length=75)),
                ('cert_instituicao', models.CharField(max_length=50)),
                ('cert_arquivo', models.FileField(upload_to='')),
                ('cert_pessoa_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
