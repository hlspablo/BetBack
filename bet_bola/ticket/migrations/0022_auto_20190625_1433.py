# Generated by Django 2.2.2 on 2019-06-25 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0021_auto_20190621_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 25, 14, 33, 27), verbose_name='Data da Aposta'),
        ),
    ]
