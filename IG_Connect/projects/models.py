# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def get_project_pic_path(instance,filename):
	return 'projects/{0}/{1}'.format(instance.projectName,filename)

# Create your models here.
class Project(models.Model) : 
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	projectName = models.CharField(max_length=50)
	projectDescription = models.TextField(max_length=500)
	shortDesc = models.CharField(max_length=25)
	projectImage = models.ImageField(upload_to=get_project_pic_path,null=True,blank=True)
	publishedDate = models.DateField(auto_now=False, auto_now_add=False)
	branchList = models.CharField(max_length=200,null=True)
	contributorsList = models.ManyToManyField(User,related_name='list_of_contributors')

	def __str__(self) : 
		return self.projectName