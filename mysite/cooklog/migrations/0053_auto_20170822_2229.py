# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0052_chef_chef_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_diagram_image',
            field=models.ImageField(upload_to='dish_diagram_images', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_diagram_image',
            field=models.ImageField(upload_to='recipe_diagram_images', null=True, blank=True),
        ),
    ]
