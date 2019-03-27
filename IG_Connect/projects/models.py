# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def get_project_pic_path(instance,filename):
	return 'projects/{0}/{1}'.format(instance.project.projectName,filename)

def get_team_pic_path(instance,filename):
	return 'projects/{0}/{1}'.format(instance.projectName,filename)

# Create your models here.
class Project(models.Model) : 
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	projectName = models.CharField(max_length=200)
	teampic = models.ImageField(upload_to=get_team_pic_path,null=True,blank=True)
	shortDesc = models.CharField(max_length=1000)
	objective = models.TextField(max_length=2000)
	drivingForce = models.TextField(max_length=1000)
	publishedDate = models.DateField(auto_now=False, auto_now_add=False)
	branchList = models.CharField(max_length=200,null=True)
	contributorsList = models.ManyToManyField(User,related_name='list_of_contributors')
	endusers = models.CharField(max_length=255)
	impact = models.TextField(max_length=500)
	awards = models.TextField(max_length=1000)
	plans = models.TextField(max_length=1000)
	projecturl = models.URLField(default=None)
	likecount = models.IntegerField(default=0)

	def __str__(self) : 
		return self.projectName

class ProjectImage(models.Model):
	project = models.ForeignKey(Project, related_name='images')
	image = models.ImageField(upload_to=get_project_pic_path,null=True,blank=True)
	##image_list = project.images.all()

class ProjectDescription(models.Model):
	project = models.OneToOneField(Project,on_delete=models.CASCADE, related_name='desc')
	materialsUsed = models.TextField(max_length=1000)
	developmentPhases = models.TextField(max_length=5000)

	def __str__(self) :
		return self.project.projectName

class ProjectLike(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.project.projectName 
