# Generated by Django 3.1.2 on 2021-07-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_subscriptions_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='pago'),
        ),
    ]