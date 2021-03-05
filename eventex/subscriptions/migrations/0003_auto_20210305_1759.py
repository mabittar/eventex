# Generated by Django 3.1.6 on 2021-03-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_hashid_subscriptions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'ordering': ('-created_at',), 'verbose_name': 'inscrição', 'verbose_name_plural': 'inscrições'},
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='cpf',
            field=models.CharField(max_length=11, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='criado em'),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='telefone'),
        ),
    ]
