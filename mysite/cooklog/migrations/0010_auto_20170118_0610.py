# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0009_dish_chef_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='date_scheduled',
            field=models.DateField(verbose_name='Date scheduled', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='dish_status',
            field=models.CharField(max_length=1, verbose_name='Dish status', choices=[('1', 'Done'), ('2', 'To-do-soon'), ('3', 'To-do-someday')], default='1'),
        ),
    ]
