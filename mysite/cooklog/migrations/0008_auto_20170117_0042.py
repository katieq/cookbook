# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0007_auto_20170117_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish_photo',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
    ]
