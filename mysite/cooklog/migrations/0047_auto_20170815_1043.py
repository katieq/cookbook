# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0046_auto_20170815_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='follower_id',
            field=models.ManyToManyField(related_name='followed_chefs', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
