# Generated by Django 4.2 on 2023-04-23 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_alter_perfiluser_per_nascimento_certificados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificados',
            name='cert_arquivo',
            field=models.FileField(blank=True, null=True, upload_to='certificados/%Y/%m/'),
        ),
    ]
