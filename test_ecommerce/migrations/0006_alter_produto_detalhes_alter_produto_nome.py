# Generated by Django 4.1.5 on 2023-04-07 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ecommerce', '0005_alter_produto_detalhes_alter_produto_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='detalhes',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=200, null=True, verbose_name='Produto'),
        ),
    ]
