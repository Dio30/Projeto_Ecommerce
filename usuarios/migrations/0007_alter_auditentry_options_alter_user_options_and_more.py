# Generated by Django 4.1.5 on 2023-04-02 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auditentry_data_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auditentry',
            options={'verbose_name': 'Falha de Autenticação', 'verbose_name_plural': 'Falhas de Autenticações'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
