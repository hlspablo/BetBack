# Generated by Django 2.2.4 on 2019-09-04 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0051_marketmodified_modification_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketmodified',
            name='modification_available',
            field=models.BooleanField(default=True),
        ),
    ]
