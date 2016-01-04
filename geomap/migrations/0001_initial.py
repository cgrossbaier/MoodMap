# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 20:17
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('choice_radius', models.IntegerField()),
                ('choice_polygon', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('map_center', models.CharField(max_length=200)),
                ('map_center_lon', models.FloatField()),
                ('map_center_lat', models.FloatField()),
                ('map_center_radius', models.FloatField()),
                ('map_polygon', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geomap.Map'),
        ),
    ]
