# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0039_auto_20170807_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_comments',
            field=models.CharField(null=True, verbose_name='Recipe comments', max_length=300, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_method',
            field=models.CharField(null=True, verbose_name='Recipe method', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe_source',
            field=models.CharField(null=True, verbose_name='Recipe source', max_length=200, blank=True),
        ),
    ]
