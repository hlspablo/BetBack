# Generated by Django 2.2.6 on 2019-10-09 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_cotationcopy_active'),
        ('utils', '0056_percentualstandardcotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='percentualstandardcotation',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Store', verbose_name='banca'),
            preserve_default=False,
        ),
    ]
