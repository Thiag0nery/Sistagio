# Generated by Django 4.2 on 2023-05-11 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0008_aluno_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiluser',
            name='tipo',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]