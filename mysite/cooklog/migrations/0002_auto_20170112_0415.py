# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish_photo',
            name='photo_source',
        ),
        migrations.AddField(
            model_name='dish_photo',
            name='dish_image',
            field=models.ImageField(default='NA', upload_to='dish_photos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dish_photo',
            name='photo_comment',
            field=models.CharField(verbose_name='Photo comment', default=0, max_length=200),
            preserve_default=False,
        ),
    ]
