# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

def get_image_path(instance,filename):
    return 'events/logo/{0}/{1}'.format(instance.name,filename)

def get_banner_path(instance,filename):
    return 'events/banner/{0}/{1}'.format(instance.name,filename)

# Create your models here.
class Content(models.Model):
	title=models.CharField(max_length=100)
	content=RichTextUploadingField()
	def __unicode__(self):
		return self.title

class ContactMember(models.Model):
	name = models.CharField(max_length=1000,blank=False)
	phone_no = models.CharField(max_length=100,blank=False)
	facebook_link = models.CharField(max_length=1000, default="#")

	def __unicode__(self):
		return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    description = models.CharField(max_length=2000)
    contents = models.ManyToManyField(Content,related_name='events', blank=True)
    timings = models.CharField(max_length=100, null = True)
    venue = models.CharField(max_length=255, null = True)
    organiser = models.CharField(max_length=100)
    unpaid_event = models.BooleanField(default=False)
    cost = models.CharField(max_length=100, null = True, blank=True)
    softreq = models.CharField(max_length=255, null=True, blank=True)
    contact_members = models.ManyToManyField(ContactMember, blank=True)
    isPublished = models.BooleanField(default = False)
    isRegisterationOpen = models.BooleanField(default = False)
    isApprovedUserListPublished = models.BooleanField(default = False)
    isEventEnded = models.BooleanField(default = False)
    banner_image=models.ImageField(upload_to=get_banner_path,null=True,blank=True)
    logo = models.ImageField(upload_to=get_image_path,null=True, blank=True)

    def __str__(self):
        return self.name + '-' + self.startdate.strftime("%Y-%m-%d")

class EventQuestion(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventQuestion')
	question = models.CharField(max_length = 300)
	description = models.CharField(max_length = 1000)
	isPublished = models.BooleanField(default = True)

	def __str__(self):
		return self.event.name + '-' + self.question

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
		return self.event.name + '-' + self.user.username

class EventQuestionResponse(models.Model):
	registerationRequest = models.ForeignKey(EventRegisterationRequest, on_delete=models.CASCADE, related_name='registerationStatus', null=True, blank=True)
	question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE, related_name='questionResponse')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	response = models.CharField(max_length = 1000)

	def __str__(self):
		return str(self.question) + '-' + self.user.username

class EventMessage(models.Model):
	status_choices = (
		(1,'Submitted'),
		(2,'Rejected'),
		(3,'Approved'),
		(4,'Participated'),
	)

	status = models.IntegerField(choices=status_choices, default=1)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	message = RichTextUploadingField()

	def __str__(self):
		return self.event.name + str(self.status)

class AwardResponse(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	stud1 = models.CharField(max_length=1000)
	stud2 = models.CharField(max_length=1000)
	stud3 = models.CharField(max_length=1000)
	stud4 = models.CharField(max_length=1000)
	titleofpaper = models.TextField()
	broadfield = models.TextField()
	abstract = models.TextField()
	conclusion = models.TextField()
	googledoc = models.TextField()
	whyaward = models.TextField()
	suggestions = models.TextField()

	def __str__(self):
		return self.user.first_name


