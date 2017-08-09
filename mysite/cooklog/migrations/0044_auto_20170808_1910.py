# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0043_bugs_bug_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugs',
            name='bug_comment',
            field=models.TextField(verbose_name='Bug comment'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_comments',
            field=models.CharField(blank=True, verbose_name='Dish review', max_length=800, null=True),
        ),
    ]
