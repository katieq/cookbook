# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0032_auto_20170803_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='extra_recipe_id',
            field=models.ManyToManyField(related_name='extra_recipe_dish', blank=True, to='cooklog.Recipe'),
        ),
        migrations.RemoveField(
            model_name='dish',
            name='recipe_id',
        ),
        migrations.AddField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(null=True, to='cooklog.Recipe', blank=True),
        ),
    ]
