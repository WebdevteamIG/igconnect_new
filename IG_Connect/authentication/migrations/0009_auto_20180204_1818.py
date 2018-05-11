# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-04 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_userprofile_isapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='branch',
            field=models.CharField(choices=[('CSE', 'Computer Science & Engineering'), ('ECE', 'Electronics and Communication Engineering'), ('MECH', 'Mechanical Engineering'), ('MME', 'Metallurgy Engineering'), ('CHE', 'Chemical Engineering'), ('CIVIL', 'Civil Engineering'), ('EEE', 'Electrical and Electronics Engineering'), ('BIO', 'Biotechnology')], max_length=10),
        ),
    ]
