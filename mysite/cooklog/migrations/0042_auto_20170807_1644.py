# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooklog', '0041_auto_20170807_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bugs',
            fields=[
                ('bug_id', models.AutoField(primary_key=True, serialize=False)),
                ('bug_comment', models.TextField(verbose_name='Site bug or feature request')),
                ('date_created', models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chef_dish_comments',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date created', default=datetime.datetime.now),
        ),
    ]
