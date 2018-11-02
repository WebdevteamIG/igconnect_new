# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Link(models.Model) :
	linkName = models.CharField(max_length=255)
	urlToPage = models.URLField(max_length=500)

	def __str__(self):
		return self.linkName

class NewsUpdate(models.Model) : 
	title = models.CharField(max_length=255)
	content = models.TextField(max_length=500)
	links = models.ManyToManyField(Link,related_name='news',blank=True)
	publishedDate = models.DateField(auto_now=False, auto_now_add=False)
	dateAdded = models.DateField(auto_now=False, auto_now_add=False)
	isPublished = models.BooleanField(default=False)

	def __str__(self):
		return self.title

def get_picture_path(instance,filename):
    return 'updates/pictures/{0}/{1}'.format(instance.name,filename)

class FbUpdate(models.Model):
	title = models.CharField(max_length=255)
	content = RichTextUploadingField()
	picture = models.ImageField(upload_to=get_picture_path, null=True, blank=True)
	



