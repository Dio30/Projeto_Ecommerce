# Generated by Django 4.1.5 on 2023-01-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ecommerce', '0004_produto_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='digital',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, default='/s', null=True, upload_to='produtos'),
        ),
    ]
