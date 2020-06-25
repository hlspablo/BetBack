# Generated by Django 2.2.4 on 2019-08-29 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0046_entry_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rulesmessage',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Store', unique=True, verbose_name='Banca'),
        ),
        migrations.AlterField(
            model_name='ticketcustommessage',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Store', unique=True, verbose_name='Banca'),
        ),
    ]