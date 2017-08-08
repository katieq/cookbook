# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0042_auto_20170807_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugs',
            name='bug_status',
            field=models.CharField(verbose_name='Bug status', choices=[('1', 'Not started'), ('2', 'Approved: on hold'), ('3', 'Fixed'), ('4', 'Denied/Ignored')], max_length=1, default='1'),
        ),
    ]
