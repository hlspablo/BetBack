# Generated by Django 2.2.7 on 2020-03-31 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0060_auto_20200329_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='creator_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_created_entries', to=settings.AUTH_USER_MODEL, verbose_name='Quem gerou o lançamento'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_entries', to=settings.AUTH_USER_MODEL, verbose_name='Cambista'),
        ),
    ]
