# Generated by Django 4.2 on 2023-06-16 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0030_alter_perfiluser_per_habilidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiluser',
            name='per_detalhe',
            field=models.TextField(blank=True),
        ),
    ]
