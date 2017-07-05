# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *
import datetime

def projects(request):
	projects = Project.objects.all();
	response = {}
	response['projects'] = projects
	if request.user.is_authenticated : 
		response['myprojects'] = Project.objects.filter(user=request.user)
	return render(request,'projects/projectListing.djt',response)

def show_project(request,projectname):
	project = Project.objects.get(projectName = projectname)
	return render(request,'projects/project_page.djt',{'project':project})

@login_required(login_url='/auth/login')
def addProject(request):
	response = {}
	if request.method=='POST' : 
		projectname = request.POST['projectName']
		
		try:
			existingProj = Project.objects.get(projectName=projectname)
			print "Name exists, select other name"
			response['errorNameExist'] = True
		except:
			project = Project()
			project.user = request.user
			project.projectName = request.POST['projectName']
			project.shortDesc = request.POST['shortDesc']
			project.objective = request.POST['objective']
			project.drivingForce = request.POST['drivingForce']
			project.publishedDate = datetime.datetime.now().strftime("%Y-%m-%d")
			project.branchList = request.POST['branches']
			project.endusers = request.POST['endusers']
			project.impact = request.POST['impact']
			project.awards = request.POST['awards']
			project.plans = request.POST['plans']
			project.teampic = request.FILES.get('teampicture')
			project.save()
			for contributor in request.POST.getlist('contributorList') :
				person = User.objects.get(username=contributor)
				project.contributorsList.add(person)

			projectDesc = ProjectDescription()
			projectDesc.project = project
			projectDesc.materialsUsed = request.POST['materials'] #Technology/Material Used
			projectDesc.developmentPhases = request.POST['phases']
			projectDesc.save()

			projectpics = request.FILES.getlist('projectpictures')
			for pic in projectpics :
				imgObj = ProjectImage()
				imgObj.image = pic
				imgObj.project = project
				imgObj.save()

			return redirect('/projects')

	response['contributors'] = User.objects.all().exclude(username=request.user.username); 
	return render(request,'projects/addProject.djt',response)

@login_required(login_url='/auth/login')
def editProject(request,projectname) :
	response = {}
	try:
		project = Project.objects.get(projectName=projectname)
		if request.method == 'POST' :
			project.shortDesc = request.POST['shortDesc']
			project.objective = request.POST['objective']
			project.drivingForce = request.POST['drivingForce']
			project.branchList = request.POST['branches']
			project.endusers = request.POST['endusers']
			project.impact = request.POST['impact']
			project.awards = request.POST['awards']
			project.plans = request.POST['plans']
			project.teampic = request.FILES.get('teampicture')
			project.save()

			projectpics = request.FILES.getlist('projectpictures')
			for pic in projectpics :
				imgObj = ProjectImage()
				imgObj.image = pic
				imgObj.project = project
				imgObj.save()
		else :
			response['project'] = project
			return render(request,'projects/editProject.djt',response)
	except:
		print "Project Doesn't exist Error"
	
	return redirect('/projects')
	
		
