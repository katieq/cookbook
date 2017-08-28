# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0053_auto_20170822_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_diagram_text',
            field=models.TextField(null=True, blank=True, verbose_name='Diagram text'),
        ),
    ]
