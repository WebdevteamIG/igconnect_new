# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def get_profilepic_path(instance,filename):
	return 'users/{0}/profilepic/{1}'.format(instance.user.first_name+"_"+instance.regNum,filename)

def get_resume_path(instance,filename):
	return 'users/{0}/resume/{1}'.format(instance.user.first_name+"_"+instance.regNum,filename)

# Create your models here.
class Userprofile(models.Model) : 
	branch_choices = (
		('CSE','Computer Science & Engineering'),
		('ECE','Electronics and Communication Engineering'),
		('MECH','Mechanical Engineering'),
		('ME','Metallurgy Engineering'),
		('CHE','Chemical Engineering'),
		('CIVIL','Civil Engineering'),
		('EEE','Electrical and Electronics Engineering'),
		('BIO','Biotechnology'),
	)

	course_choices = (
		('BTech','B.Tech'),
		('MTech','M.Tech'),
		('MCA','MCA'),
		('MBA','MBA'),
		('PHD','Phd'),
	)

	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	regNum = models.CharField(max_length=10)
	course = models.CharField(max_length=10,choices = course_choices,default='BTech')
	branch = models.CharField(max_length=10,choices = branch_choices)
	contact = models.CharField(max_length=20)
	aboutMe = models.CharField(max_length=200)
	profile_pic = models.ImageField(upload_to=get_profilepic_path,null=True,blank=True)
	resume = models.FileField(upload_to=get_resume_path,null=True,blank=True)

	def __str__(self):
		return (self.user.first_name + "_" + self.regNum)