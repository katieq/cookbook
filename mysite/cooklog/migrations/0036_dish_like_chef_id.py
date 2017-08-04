# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0035_auto_20170804_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='like_chef_id',
            field=models.ManyToManyField(related_name='chef_like', blank=True, to='cooklog.Chef'),
        ),
    ]
