# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
import smtplib
import datetime

# Create your views here.

def index(request):
	response = {}
	response["components"] = Component.objects.all()
	return render(request, 'hardware/index.html', response)

def buynow(request):
	response = {}
	if request.method == "POST":
		product_id = request.POST["id"]
		component = Component.objects.get(pk=product_id)
		print(component)
		user = request.user 
		message = str(component.name) + '\n'
		message+=str(component.price)
		message+=str(user.username) + " has taken the above component on "
		message+=str(datetime.datetime.now())
		sender = "ig-nitw@studexnt.nitw.ac.in"
		receiver = 'ch1sai2teja3@gmail.com'
		rlist = []
		rlist.append(receiver)
		send_mail('IG Connect Hardware Shop',message,sender,rlist,fail_silently=False,)
		response["component"] = component

	return render(request, "hardware/buynow.html", response)

def lend(request):
	response = {}
	if request.method == "POST":
		product_id = request.POST["id"]
		component = Component.objects.get(pk=product_id)
		user = request.user
		lendComp = ComponentLending()
		lendComp.user = user
		lendComp.component = component
		lendComp.dateTaken = datetime.datetime.now()
		lendComp.save()
		response["component"] = component
	return render(request, "hardware/lend.html", response)

def lendedComponents(request):
	response = {}
	lended_comp = ComponentLending.objects.filter(user=request.user)
	dates = []
	for comp in lended_comp:
		r = {}
		days = datetime.datetime.now().date() - comp.dateTaken
		days = days.total_seconds()/60/60/24
		days = 14 - int(days)
		dates.append(r)
		r["days"] = days
	response["dates"] = dates
	response["lended_comp"] = lended_comp
	response["zipped"] = zip(dates, lended_comp)
	return render(request, "hardware/lended.html", response)

# admin
# all users lended component
# renewall date 
# all users contact

def admin(request):
	response = {}
	lended_comp = ComponentLending.objects.all()
	response["lended_comp"] = lended_comp
	dates = []
	for comp in lended_comp:
		r = {}
		days = datetime.datetime.now().date() - comp.dateTaken
		days = days.total_seconds()/60/60/24
		days = 14 - int(days)
		dates.append(r)
		r["days"] = days
	response["dates"] = dates
	response["zipped"] = zip(dates, lended_comp)
	return render(request, "hardware/admin.html", response)

def return_item(request):
	if request.POST["type"] == "return" :
		ComponentLending.objects.get(pk=request.POST["item"]).delete()
		return redirect("/hardware/admin")
	if request.POST["type"] == "renew" :
		component = ComponentLending.objects.get(pk=request.POST["item"])
		component.dateTaken = datetime.datetime.now()
		component.save()
		return redirect("/hardware/admin")
	if request.POST["type"] == "add"  :
		component = Component()
		component.name = request.POST["name"]
		component.price = int(request.POST["price"])
		component.save()		
		return redirect("/hardware")








