# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('chef_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(verbose_name='Email address', max_length=50)),
                ('first_name', models.CharField(verbose_name='First name', max_length=30)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=30)),
                ('date_created', models.DateTimeField(verbose_name='Date created')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('dish_id', models.AutoField(primary_key=True, serialize=False)),
                ('dish_name', models.CharField(verbose_name='Dish name', max_length=200)),
                ('dish_method', models.CharField(verbose_name='Dish method', max_length=800)),
                ('dish_rating', models.IntegerField(default=0)),
                ('dish_comments', models.CharField(verbose_name='Dish comments', max_length=800)),
                ('date_created', models.DateTimeField(verbose_name='Date created')),
            ],
        ),
        migrations.CreateModel(
            name='Dish_Photo',
            fields=[
                ('dish_photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('photo_source', models.CharField(verbose_name='Photo url', max_length=200)),
                ('date_created', models.DateTimeField(verbose_name='Date created')),
                ('dish_id', models.ForeignKey(to='cooklog.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('ingredient_id', models.AutoField(primary_key=True, serialize=False)),
                ('ingredient_name', models.CharField(verbose_name='Ingredient name', max_length=30)),
                ('ingredient_type', models.CharField(verbose_name='Ingredient type', max_length=30)),
                ('date_created', models.DateTimeField(verbose_name='Date created')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('recipe_id', models.AutoField(primary_key=True, serialize=False)),
                ('recipe_name', models.CharField(verbose_name='Recipe name', max_length=200)),
                ('recipe_source', models.CharField(verbose_name='Recipe source', max_length=200)),
                ('recipe_type', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(verbose_name='Date created')),
                ('chef_id', models.ForeignKey(to='cooklog.Chef')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredient_id',
            field=models.ManyToManyField(to='cooklog.Ingredient'),
        ),
        migrations.AddField(
            model_name='dish',
            name='recipe_id',
            field=models.ForeignKey(to='cooklog.Recipe'),
        ),
    ]
