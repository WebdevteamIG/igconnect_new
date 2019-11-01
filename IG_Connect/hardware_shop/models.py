# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Component(models.Model):
	name = models.CharField(max_length=255)
	available = models.BooleanField(default=True)
	price = models.IntegerField(default=50)

	def __str__(self):
		return self.name

class ComponentLending(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	component = models.ForeignKey(Component,on_delete=models.CASCADE)
	dateTaken = models.DateField()

	def __str__(self):
		return self.component.name + " by " + self.user.username
