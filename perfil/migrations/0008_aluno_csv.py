# Generated by Django 4.2 on 2023-05-10 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0007_perfiluser_cpf_cnpj_perfiluser_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno_Csv',
            fields=[
                ('alu_codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('alu_nome', models.CharField(max_length=50)),
                ('alu_matricula', models.CharField(max_length=20)),
                ('alu_turma', models.CharField(max_length=20)),
            ],
        ),
    ]