# Generated by Django 4.2 on 2023-05-23 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_vagas', '0005_alter_postvagas_vag_perfil_fk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postvagas',
            old_name='vag_perfil_fk',
            new_name='vag_usuario_fk',
        ),
    ]