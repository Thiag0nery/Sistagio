# Generated by Django 4.2 on 2023-06-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_vagas', '0007_alter_postvagas_vag_beneficio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postvagas',
            name='vag_beneficio',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='postvagas',
            name='vag_descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postvagas',
            name='vag_endereco',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='postvagas',
            name='vag_funcao',
            field=models.TextField(blank=True, null=True),
        ),
    ]