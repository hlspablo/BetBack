# Generated by Django 2.2.4 on 2019-08-26 17:28

from django.db import migrations, models
import utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0022_auto_20190820_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credittransactions',
            name='transaction_date',
            field=models.DateTimeField(default=utils.timezone.now, verbose_name='Data da Transação'),
        ),
        migrations.AlterField(
            model_name='managercashierhistory',
            name='date',
            field=models.DateTimeField(default=utils.timezone.now, verbose_name='Data da Transação'),
        ),
        migrations.AlterField(
            model_name='sellercashierhistory',
            name='date',
            field=models.DateTimeField(default=utils.timezone.now, verbose_name='Data da Transação'),
        ),
    ]