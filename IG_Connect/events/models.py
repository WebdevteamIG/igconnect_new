# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    eventName = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    description = models.CharField(max_length=50)
    organiser = models.CharField(max_length=50)

    def __str__(self):
        return self.eventName