# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0011_auto_20170118_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dish_method',
            field=models.CharField(max_length=800, verbose_name='Dish method', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_rating',
            field=models.IntegerField(verbose_name='Dish rating', null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], blank=True),
        ),
    ]
