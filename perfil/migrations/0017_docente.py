# Generated by Django 4.2 on 2023-05-24 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0016_alter_certificados_cert_pessoa_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('doce_codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('doce_perfil_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.perfiluser')),
            ],
        ),
    ]