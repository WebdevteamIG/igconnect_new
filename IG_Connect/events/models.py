# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Event(models.Model):
    eventName = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    description = models.CharField(max_length=2000)
    timings = models.CharField(max_length=100, null = True)
    organiser = models.CharField(max_length=100)
    isPublished = models.BooleanField(default = False)
    isRegisterationOpen = models.BooleanField(default = True)
    isApprovedUserListPublished = models.BooleanField(default = False)
    isEventEnded = models.BooleanField(default = False)

    def __str__(self):
        return self.eventName + '-' + self.startdate.strftime("%Y-%m-%d")

class EventQuestion(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventQuestion')
	question = models.CharField(max_length = 300)
	description = models.CharField(max_length = 1000)
	isPublished = models.BooleanField(default = True)

	def __str__(self):
		return self.event.eventName + '-' + self.question

class EventRegisterationRequest(models.Model):
	status_choices = (
		(1,'Submitted'),
		(2,'Rejected'),
		(3,'Approved'),
		(4,'Participated'),
	)

	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventRegRequest')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	requestDate = models.DateTimeField()
	status = models.IntegerField(choices=status_choices,default=1)

	def __str__(self):
		return self.event.eventName + '-' + self.user.username

class EventQuestionResponse(models.Model):
	question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE, related_name='questionResponse')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	response = models.CharField(max_length = 1000)

	def __str__(self):
		return str(self.question) + '-' + self.user.username

