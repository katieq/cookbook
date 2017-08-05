# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0037_auto_20170804_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, to='cooklog.Recipe', default=1),
        ),
    ]
