# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from projects.models import *
from .models import *
import datetime

def checkuserifsuperuser(user):
    if user.is_superuser:
        return True
    else:
        return False


@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/')
def dashboard(request) :
	response = {}
	response['updates'] = NewsUpdate.objects.all()
	return render(request,'updates/dashboard.djt',response)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/')
def addNews(request) :
	response = {}
	if request.method == 'POST' :
		news = NewsUpdate()
		news.title = request.POST['title']
		news.content = request.POST['content']
		news.dateAdded = datetime.datetime.now().strftime("%Y-%m-%d")
		news.publishedDate = datetime.datetime.now().strftime("%Y-%m-%d")
		news.isPublished = True
		news.save()

		if request.POST.get('fbLink') :
			fbLink = Link()
			fbLink.linkName = request.POST['fblinkName']
			fbLink.urlToPage = request.POST['fburlToPage']
			fbLink.save()
			news.links.add(fbLink)
		if request.POST.get('otherLink') :
			otherLink = Link()
			otherLink.linkName = request.POST['linkName']
			otherLink.urlToPage = request.POST['urlToPage']
			otherLink.save()
			news.links.add(otherLink)

		return redirect('/updates')


	return render(request,'updates/addNews.djt',response)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/')
def publishNews(request,id) :
	response = {}
	news = NewsUpdate.objects.get(id=id)
	news.isPublished = True
	news.publishedDate = datetime.datetime.now().strftime("%Y-%m-%d")
	news.save()
	return redirect('/updates')

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/')
def unPublishNews(request,id) :
	response = {}
	news = NewsUpdate.objects.get(id=id)
	news.isPublished = False
	news.save()
	return redirect('/updates')

def fbScrape(request):
	response = {}
	