# Generated by Django 2.2.2 on 2019-06-17 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0016_auto_20190617_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 17, 16, 18, 4), verbose_name='Data da Aposta'),
        ),
    ]