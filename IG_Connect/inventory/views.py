# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *
from authentication.models import *
import datetime

def checkuserifsuperuser(user):
    if user.is_superuser:
        return True
    else:
        return False

def checkuserifallowed(user):
	borrowedItems = ItemRequest.objects.filter(user = user)
	countOfItems = len(borrowedItems)
	if countOfItems<4 and user.profile.isApproved:
		return True
	else:
		return False

# Create your views here.
@login_required(login_url='/auth/login')	
def listItems(request) :
	response = {}
	response['items'] = Item.objects.all()
	borrowedItems = ItemRequest.objects.filter(user=request.user)
	countOfItems = len(borrowedItems)
	if countOfItems<4 :
		response['allowed'] = True
	else :
		response['allowed'] = False
	return render(request,'inventory/listPage.djt',response)

@user_passes_test(checkuserifsuperuser, login_url='/')
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

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifallowed, login_url='/auth/login')
def requestItem(request,id) :
	response = {}
	try:
		item = Item.objects.get(id=id)
		item.status = 2
		item.save()
		print "item modified"

		requestObj = ItemRequest()
		requestObj.user = request.user
		requestObj.item = item
		requestObj.dateOfRequest = datetime.datetime.now().strftime("%Y-%m-%d")
		# requestObj.approvalDate = datetime.datetime.now().strftime("%Y-%m-%d")
		requestObj.save()
		print

		logObj = requestActionLog()
		logObj.item = item
		logObj.user = request.user
		logObj.dateOfAction = datetime.datetime.now().strftime("%Y-%m-%d")
		logObj.content = 'Request Made by user'
		logObj.save()

	except Exception as e :
		print e
		return HttpResponse("There is no such Item, Sorry :) !!!")

	return redirect('/borrow')

@user_passes_test(checkuserifsuperuser, login_url='/')
def approveItemRequest(request,id) :
	response = {}
	item = Item.objects.get(id=id)
	requestObj = ItemRequest.objects.get(item=item)
	item.status = 3
	item.save()
	requestObj.approvalDate = datetime.datetime.now().strftime("%Y-%m-%d")
	requestObj.returnDate = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
	requestObj.save()

	logObj = requestActionLog()
	logObj.item = item
	logObj.user = requestObj.user
	logObj.dateOfAction = datetime.datetime.now().strftime("%Y-%m-%d")
	logObj.content = 'Request Approved by admin'
	logObj.save()

	return redirect('/borrow/listRequests')

@login_required(login_url='/auth/login')
def cancelItemRequest(request,id) : 
	response = {}
	try:
		item = Item.objects.get(id=id)
		requestObj = ItemRequest.objects.get(item=item)
		if requestObj.user == request.user:
			item.status = 1
			item.save()

			logObj = requestActionLog()
			logObj.item = item
			logObj.user = request.user
			logObj.dateOfAction = datetime.datetime.now().strftime("%Y-%m-%d")
			logObj.content = 'Request Cancelled by user'
			logObj.save()

			requestObj.delete()
	except:
		print( "Error while cencelling item request" )
	return redirect('/borrow')

@user_passes_test(checkuserifsuperuser, login_url='/')
def getItemBack(request,id,Actiontype) : 
	response = {}
	item = Item.objects.get(id=id)
	requestObj = ItemRequest.objects.get(item=item)
	item.status = 1
	item.save()

	logObj = requestActionLog()
	logObj.item = item
	logObj.user = requestObj.user
	logObj.dateOfAction = datetime.datetime.now().strftime("%Y-%m-%d")
	if Actiontype == '1' :
		logObj.content = 'Request Rejected by admin'
	else :
		logObj.content = 'Item returned and collected safely'
	logObj.save()

	requestObj.delete()

	return redirect('/borrow/listRequests')

@user_passes_test(checkuserifsuperuser, login_url='/')
def listRequests(request) :
	response = {}
	response['itemRequests'] = ItemRequest.objects.all()
	return render(request,'inventory/requestHandlePage.djt',response)

@user_passes_test(checkuserifsuperuser, login_url='/')
def viewLogs(request) :
	response = {}
	response['logs'] = requestActionLog.objects.all()
	return render(request,'inventory/logsPage.djt',response)

@user_passes_test(checkuserifsuperuser, login_url='/')
def initialApproval(request) :
	response = {}
	response['pendingUsers'] = Userprofile.objects.filter(isApproved=False)
	return render(request,'inventory/initialApprovalPage.djt',response)

@user_passes_test(checkuserifsuperuser, login_url='/')
def approveUser(request,regNum) : 
	response = {}
	try :
		userProfile = Userprofile.objects.get(regNum=regNum)
		userProfile.isApproved = True
		userProfile.save()
	except :
		print "error occured while approving user"
	return redirect('/borrow/initialApproval')

@login_required(login_url='/auth/login')
def borrowedItems(request) : 
	response = {}
	response['borrowedItems'] = ItemRequest.objects.filter(user=request.user)
	return render(request,'inventory/borrowedItems.djt',response)
