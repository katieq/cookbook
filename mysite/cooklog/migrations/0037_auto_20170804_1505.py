# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0036_dish_like_chef_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='chef_id',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='dish_id',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
