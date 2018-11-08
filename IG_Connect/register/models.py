# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class Form(models.Model):
    title = models.CharField(max_length=255)
    choice = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return self.title

class Registered(models.Model):
    title = models.ForeignKey(Form)
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=3)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    Regno = models.CharField(max_length=18)

    def __str__(self):
        return self.title.title + "_" + str(self.title.choice)

class SendInfo(models.Model):
    name = models.CharField(max_length=255)
    ctc = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return self.name
        
