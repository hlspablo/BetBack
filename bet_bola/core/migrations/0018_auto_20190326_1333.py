# Generated by Django 2.1.7 on 2019-03-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20190326_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotation',
            name='settlement',
            field=models.IntegerField(blank=True, choices=[(0, 'Em Aberto'), (-1, 'Cancelada'), (1, 'Perdeu'), (2, 'Ganhou'), (3, 'Perdeu'), (4, 'Perdeu'), (5, 'Ganhou')], default=0, null=True, verbose_name='Resultado'),
        ),
    ]