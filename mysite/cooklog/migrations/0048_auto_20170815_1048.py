# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooklog', '0047_auto_20170815_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefFollows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date_created', models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='chef',
            name='follower_id',
        ),
        migrations.AddField(
            model_name='cheffollows',
            name='chef_id',
            field=models.ManyToManyField(to='cooklog.Chef', related_name='followed_by'),
        ),
        migrations.AddField(
            model_name='cheffollows',
            name='follower_id',
            field=annoying.fields.AutoOneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
