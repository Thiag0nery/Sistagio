# Generated by Django 4.2 on 2023-06-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0020_alter_aluno_csv_alu_vinculado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiluser',
            name='cpf_cnpj',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]