# Generated by Django 2.2.7 on 2020-03-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_manager_can_close_cashier'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='can_add_entry',
            field=models.BooleanField(default=True, verbose_name='Pode adicionar Lançamento ?'),
        ),
    ]
