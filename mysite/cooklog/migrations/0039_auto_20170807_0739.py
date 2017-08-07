# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0038_auto_20170804_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_type',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='chef_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='cooklog.Chef'),
        ),
    ]
