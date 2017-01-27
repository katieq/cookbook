# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0010_auto_20170118_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dish_comments',
            field=models.CharField(blank=True, verbose_name='Dish comments', max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
