# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0050_recipe_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag', blank=True),
        ),
    ]
