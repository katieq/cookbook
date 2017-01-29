# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0012_auto_20170118_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_source',
            field=models.CharField(verbose_name='Recipe source', max_length=200, null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='dish_photo',
            name='dish_id',
        ),
        migrations.AddField(
            model_name='dish_photo',
            name='dish_id',
            field=models.ManyToManyField(to='cooklog.Dish'),
        ),
    ]
