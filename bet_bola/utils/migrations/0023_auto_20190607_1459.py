# Generated by Django 2.2.2 on 2019-06-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0022_managercomission_profit_comission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalconfigurations',
            name='auto_pay_punter',
        ),
        migrations.AddField(
            model_name='generalconfigurations',
            name='auto_pay_winners',
            field=models.BooleanField(default=True, verbose_name='Auto Pagar Ganhadores'),
        ),
    ]