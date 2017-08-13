# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cooklog', '0044_auto_20170808_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(blank=True, upload_to='recipe_photos', null=True),
        ),
        migrations.AlterField(
            model_name='bugs',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, related_name='user_bug', on_delete=django.db.models.deletion.SET_DEFAULT),
        ),
        migrations.AlterField(
            model_name='chef_dish_comments',
            name='chef_id',
            field=models.ForeignKey(to='cooklog.Chef', default=1, related_name='comment_by_chef'),
        ),
        migrations.AlterField(
            model_name='chef_dish_comments',
            name='dish_id',
            field=models.ForeignKey(to='cooklog.Dish', related_name='comment_about_dish'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='chef_id',
            field=models.ForeignKey(to='cooklog.Chef', default=1, related_name='cooked_by_chef'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_comments',
            field=models.TextField(verbose_name='Dish review', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_method',
            field=models.TextField(verbose_name='Dish method', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(to='cooklog.Recipe', default=1, related_name='instance_of_recipe', on_delete=django.db.models.deletion.SET_DEFAULT),
        ),
    ]
