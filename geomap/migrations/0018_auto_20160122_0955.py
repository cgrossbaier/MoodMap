# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geomap', '0017_auto_20160121_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(verbose_name='Created'),
        ),
    ]
