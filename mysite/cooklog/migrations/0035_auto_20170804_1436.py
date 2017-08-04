# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0034_auto_20170803_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(default=1, to='cooklog.Recipe'),
        ),
    ]
