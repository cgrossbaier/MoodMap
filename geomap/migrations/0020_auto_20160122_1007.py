# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geomap', '0019_auto_20160122_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(verbose_name='Created'),
        ),
    ]