# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0040_auto_20170807_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_comments',
            field=models.TextField(blank=True, null=True, verbose_name='Recipe comments'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe_method',
            field=models.TextField(blank=True, null=True, verbose_name='Recipe method'),
        ),
    ]
