# Generated by Django 5.0 on 2023-12-12 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogos', '0002_alter_jogo_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogo',
            name='descricao',
            field=models.TextField(max_length=50),
        ),
    ]
