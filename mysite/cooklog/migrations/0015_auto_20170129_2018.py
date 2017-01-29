# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0014_auto_20170129_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('chef_id', models.ForeignKey(to='cooklog.Chef')),
            ],
        ),
        migrations.RemoveField(
            model_name='dish',
            name='likes_id',
        ),
        migrations.AddField(
            model_name='likes',
            name='dish_id',
            field=models.ForeignKey(to='cooklog.Dish'),
        ),
    ]
