# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 16:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geomap', '0003_event_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='lon',
            new_name='lng',
        ),
    ]