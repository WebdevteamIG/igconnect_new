# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *

def projects(request):
	projects = Project.objects.all();
	return render(request,'projects/projectListing.djt',{'projects':projects})

def show_project(request):
	project = Project.objects.get(id=1)
	return render(request,'projects/project_page.html',{'proj':project})
