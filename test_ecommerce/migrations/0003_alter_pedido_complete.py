# Generated by Django 4.1.5 on 2023-01-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ecommerce', '0002_alter_pedido_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='complete',
            field=models.BooleanField(default=False, null=True, verbose_name='Pedido Completado'),
        ),
    ]
