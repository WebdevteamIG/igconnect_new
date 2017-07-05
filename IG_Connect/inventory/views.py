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

# Create your views here.
def listItems(request) :
	response = {}
	response['items'] = Item.objects.all()
	return render(request,'inventory/listPage.djt',response)

def addItem(request) :
	response= {}
	if request.method == 'POST' :
		item = Item()
		item.itemName = request.POST['itemName']
		item.status = 1
		item.itemType = request.POST['itemType']
		item.save()
		return redirect('/borrow')
	return render(request,'inventory/addItem.djt',response)

def requestItem(request,id) :
	response = {}
	try:
		item = Item.objects.get(id=id)
		item.status = 2
		item.save()

		requestObj = ItemRequest()
		requestObj.user = request.user
		requestObj.item = item
		requestObj.dateOfRequest = datetime.datetime.now().strftime("%Y-%m-%d")
		requestObj.approvalDate = datetime.datetime.now().strftime("%Y-%m-%d")
		requestObj.save()

	except Exception as e :
		print e
		return HttpResponse("There is no such Item, Sorry :) !!!")

	return redirect('/borrow')

def approveItemRequest(request,id) :
	response = {}
	item = Item.objects.get(id=id)
	requestObj = ItemRequest.objects.get(item=item)
	item.status = 3
	item.save()
	requestObj.approvalDate = datetime.datetime.now().strftime("%Y-%m-%d")
	requestObj.save()

	return redirect('/borrow/listRequests')

def cancelItemRequest(request,id) : 
	response = {}
	item = Item.objects.get(id=id)
	requestObj = ItemRequest.objects.get(item=item)
	item.status = 1
	item.save()
	requestObj.delete()

	return redirect('/borrow')

def getItemBack(request,id) : 
	response = {}
	item = Item.objects.get(id=id)
	requestObj = ItemRequest.objects.get(item=item)
	item.status = 1
	item.save()
	requestObj.delete()

	return redirect('/borrow/listRequests')

def listRequests(request) :
	response = {}
	response['itemRequests'] = ItemRequest.objects.all()
	return render(request,'inventory/requestHandlePage.djt',response)