# Generated by Django 4.2 on 2023-04-22 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_alter_perfiluser_per_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiluser',
            name='per_nascimento',
            field=models.DateField(),
        ),
    ]
