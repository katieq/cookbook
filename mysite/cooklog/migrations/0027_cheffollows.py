# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-28 17:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooklog', '0026_auto_20170706_0316'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefFollows',
            fields=[
                ('chef_follow_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date created')),
                ('chef_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooklog.Chef')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]