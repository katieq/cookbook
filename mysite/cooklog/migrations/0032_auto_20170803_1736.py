# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-04 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0031_auto_20170803_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='recipe_id',
        ),
        migrations.AddField(
            model_name='dish',
            name='recipe_id',
            field=models.ManyToManyField(blank=True, to='cooklog.Recipe'),
        ),
    ]
