# Generated by Django 4.2 on 2023-05-23 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post_vagas', '0004_vaga_cadastradas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postvagas',
            name='vag_perfil_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]