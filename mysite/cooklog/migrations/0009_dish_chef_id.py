# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0008_auto_20170117_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='chef_id',
            field=models.ForeignKey(default=1, to='cooklog.Chef'),
        ),
    ]
