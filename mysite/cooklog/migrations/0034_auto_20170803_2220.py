# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0033_auto_20170803_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(to='cooklog.Recipe', default=1),
            preserve_default=False,
        ),
    ]
