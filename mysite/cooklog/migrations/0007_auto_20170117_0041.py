# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0006_auto_20170117_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='dish',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
    ]
