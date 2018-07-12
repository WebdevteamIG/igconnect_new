# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Experience(models.Model):
    projectName = models.CharField(max_length=255)
    contributors = models.CharField(max_length=500)
    exp = models.TextField(max_length=50000)

    def __str__(self):
        return self.projectName



