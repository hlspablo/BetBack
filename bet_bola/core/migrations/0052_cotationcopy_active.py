# Generated by Django 2.2.6 on 2019-10-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20190919_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotationcopy',
            name='active',
            field=models.BooleanField(default=True, verbose_name='ativa?'),
        ),
    ]
