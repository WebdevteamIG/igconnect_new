# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-23 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventregisterationrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventquestionresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionResponse', to='events.EventQuestion'),
        ),
    ]
