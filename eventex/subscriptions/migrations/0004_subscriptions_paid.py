# Generated by Django 3.1.2 on 2021-07-22 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20210305_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]