# Generated by Django 2.1.7 on 2019-05-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20190506_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymoususer',
            name='cellphone',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='Celular'),
        ),
    ]