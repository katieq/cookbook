# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-01 04:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0021_auto_20170201_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='chef_to_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]