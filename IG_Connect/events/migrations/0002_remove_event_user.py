# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-22 06:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
    ]
