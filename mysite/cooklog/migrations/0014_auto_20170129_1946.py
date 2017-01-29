# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0013_auto_20170129_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chef_Dish_Comments',
            fields=[
                ('chef_dish_comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('chef_dish_comment', models.CharField(max_length=800, verbose_name='Chef dish comment')),
                ('chef_id', models.ForeignKey(to='cooklog.Chef', default=1)),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='likes_id',
            field=models.ManyToManyField(to='cooklog.Chef', related_name='likes'),
        ),
        migrations.AddField(
            model_name='chef_dish_comments',
            name='dish_id',
            field=models.ForeignKey(to='cooklog.Dish'),
        ),
    ]
