# Generated by Django 2.2.2 on 2019-07-01 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0011_auto_20190701_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managertransactions',
            name='manager',
        ),
        migrations.AddField(
            model_name='managertransactions',
            name='creditor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='credit_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Gerente'),
            preserve_default=False,
        ),
    ]
