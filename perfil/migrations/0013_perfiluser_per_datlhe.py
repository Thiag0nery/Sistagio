# Generated by Django 4.2 on 2023-05-22 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0012_perfiluser_per_tell'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfiluser',
            name='per_datlhe',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
