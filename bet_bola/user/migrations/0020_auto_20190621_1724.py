# Generated by Django 2.2.2 on 2019-06-21 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_remove_manager_profit_comission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='credit_limit_to_add',
            new_name='credit_limit',
        ),
    ]
