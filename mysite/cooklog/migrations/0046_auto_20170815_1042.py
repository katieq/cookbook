# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooklog', '0045_auto_20170813_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cheffollows',
            name='chef_id',
        ),
        migrations.RemoveField(
            model_name='cheffollows',
            name='follower_id',
        ),
        migrations.AddField(
            model_name='chef',
            name='follower_id',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='followed_chefs', null=True),
        ),
        migrations.DeleteModel(
            name='ChefFollows',
        ),
    ]
