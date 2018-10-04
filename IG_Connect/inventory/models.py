# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Item(models.Model) :
	status_choices = (
		(1,'Available'),
		(2,'Requested'),
		(3,'Borrowed'),
	)

	itemType = models.CharField(max_length=20)
	status = models.IntegerField(choices=status_choices,default=1)
	itemName = models.CharField(max_length=255)

	def __str__(self) :
		return self.itemName

class ItemRequest(models.Model) :
	user = models.ForeignKey(User,related_name='requestedItem')
	dateOfRequest = models.DateField(auto_now=False, auto_now_add=False)
	item = models.ForeignKey(Item,related_name='correspondingRequest')
	approvalDate = models.DateField(auto_now=False, auto_now_add=False, null = True)
	returnDate = models.DateField(auto_now=False, auto_now_add=False, null = True)

	def __str__(self) :
		return (self.user.username + "-" + self.item.itemName)

class requestActionLog(models.Model) :
	item = models.ForeignKey(Item)
	user = models.ForeignKey(User,related_name='logs')
	dateOfAction = models.DateField(auto_now=False, auto_now_add=False)
	content = models.CharField(max_length=255)

	def __str__(self) :
		return (self.user.username+" "+self.item.itemName+" "+self.content)