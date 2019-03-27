# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-27 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('available', models.BooleanField(default=True)),
                ('price', models.IntegerField(default=50)),
            ],
        ),
    ]
