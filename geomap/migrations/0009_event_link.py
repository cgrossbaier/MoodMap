# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geomap', '0008_auto_20160113_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]
