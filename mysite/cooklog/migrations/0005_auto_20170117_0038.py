# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0004_auto_20170112_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='dish_photo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date created'),
        ),
    ]
