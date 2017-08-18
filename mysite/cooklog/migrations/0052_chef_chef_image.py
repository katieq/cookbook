# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0051_auto_20170815_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='chef',
            name='chef_image',
            field=models.ImageField(blank=True, upload_to='chef_photos', null=True),
        ),
    ]
