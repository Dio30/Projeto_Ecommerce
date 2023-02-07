# Generated by Django 4.1.5 on 2023-02-07 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now=True, verbose_name='Data do pedido')),
                ('complete', models.BooleanField(default=False, verbose_name='Pedido foi Completado')),
                ('id_transacao', models.CharField(max_length=100, verbose_name='Código da Transação')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, null=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=7)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produtos')),
                ('digital', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(blank=True, default=0, null=True)),
                ('data_adicao', models.DateTimeField(auto_now=True)),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_ecommerce.pedido')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_ecommerce.produto')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
            },
        ),
        migrations.CreateModel(
            name='EnderecoEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(max_length=200, null=True)),
                ('cidade', models.CharField(max_length=200, null=True)),
                ('bairro', models.CharField(max_length=200, null=True)),
                ('estado', models.CharField(max_length=200, null=True)),
                ('cep', models.CharField(max_length=200, null=True)),
                ('data_adicao', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_ecommerce.pedido')),
            ],
        ),
    ]
