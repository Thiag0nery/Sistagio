# Generated by Django 4.2 on 2023-06-09 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0027_avaliacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='ava_pergunta_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='perfil.perguntas'),
        ),
    ]
