# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *

def checkuserifsuperuser(user):
    if user.is_superuser:
        return True
    else:
        return False

# Create your views here.
def eventsHome(request) :
	response = {}
	response['events'] = Event.objects.filter(isPublished = True)
	return render(request,'events/eventsHomepage.djt',response)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/')
def addEvent(request) :
	response= {}
	if request.method == 'POST' :
		event = Event()
		event.eventName = request.POST['eventName']
		event.description = request.POST['description']
		event.timings = request.POST['timings']
		event.organiser = request.POST['organiser']
		event.startdate = datetime.strptime(request.POST['startDate'], '%Y-%m-%d')
		event.enddate = datetime.strptime(request.POST['endDate'], '%Y-%m-%d')
		event.save()
		return redirect('/events/manageevent/%d'%event.pk)
	return render(request,'events/addEvent.djt',response)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
def manageEvent(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		questions = EventQuestion.objects.filter(event = event)
		response['event'] = event
		response['questions'] = questions
		return render(request,'events/manageEvent.djt',response)
	except:
		print("Error occured while managing event.")
	return redirect('/events')

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
def editEvent(request,id) :
	response= {}
	event = Event.objects.get(id=id)
	if request.method == 'POST' :
		event.eventName = request.POST['eventName']
		event.description = request.POST['description']
		event.timings = request.POST['timings']
		event.organiser = request.POST['organiser']
		event.startdate = datetime.strptime(request.POST['startDate'], '%Y-%m-%d')
		event.enddate = datetime.strptime(request.POST['endDate'], '%Y-%m-%d')
		if request.POST.get('eventPublished'):
			event.isPublished = True
		else:
			event.isPublished = False

		if request.POST.get('registerationOpen'):
			event.isRegisterationOpen = True
		else:
			event.isRegisterationOpen = False

		if request.POST.get('userListPublished'):
			event.isApprovedUserListPublished = True
		else:
			event.isApprovedUserListPublished = False

		if request.POST.get('eventEnded'):
			event.isEventEnded = True
		else:
			event.isEventEnded = False

		event.save()
		return redirect('/events/manageevent/%d'%event.pk)

	questions = EventQuestion.objects.filter(event = event)
	response['event'] = event
	response['questions'] = questions
	response['startdate'] = event.startdate.strftime("%Y-%m-%d")
	response['enddate'] = event.enddate.strftime("%Y-%m-%d")
	return render(request,'events/editEvent.djt',response)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
def addQuestion(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		question = EventQuestion()
		question.event = event
		question.question = request.POST['question']
		question.description = request.POST['quesDescription']
		question.save()
		return redirect('/events/manageevent/%d'%event.pk)
	except:
		print("Error occured while managing event.")
	return redirect('/events')

def viewEvent(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		response['event'] = event
		if request.user.is_authenticated() and EventRegisterationRequest.objects.filter(event = event, user = request.user).count() > 0:
			regRequest = EventRegisterationRequest.objects.get(event = event, user = request.user)
			response['regRequest'] = regRequest
		return render(request,'events/EventPage.djt',response)
	except:
		return redirect('/events')

@login_required(login_url='/auth/login')
def registerEvent(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		questions = EventQuestion.objects.filter(event = event)

		# get registeration status if exist
		isUserRegistered = False

		if EventRegisterationRequest.objects.filter(event = event, user = request.user).count() > 0:
			regRequest = EventRegisterationRequest.objects.get(event = event, user = request.user)
			isUserRegistered = True
			for question in questions:
				question.response = EventQuestionResponse.objects.get(question = question, user = request.user).response

		if event.isRegisterationOpen:
			if request.method == 'POST' :
				#Get answers and create new object if not exist or update
				print("post")

				#validating that all answers are present
				valid = True
				for question in questions:
					if request.POST.get('ques%d'%question.pk):
						question.response = request.POST['ques%d'%question.pk]
					else:
						valid = False

				if valid:
					# Response already exist, updating
					if isUserRegistered:
						for question in questions:
							quesResponse = EventQuestionResponse.objects.get(question = question, user = request.user)
							quesResponse.response = question.response
							quesResponse.save()
					# Creating new response
					else:
						regRequest = EventRegisterationRequest()
						regRequest.event = event
						regRequest.user = request.user
						regRequest.requestDate = datetime.now()
						regRequest.save()

						for question in questions:
							quesResponse = EventQuestionResponse()
							quesResponse.question = question
							quesResponse.user = request.user
							quesResponse.response = question.response
							quesResponse.save()
					response['message'] = "Response saved successfully."
				else:
					response['message'] = "Unable to save response"
				
		response['event'] = event
		response['questions'] = questions
		if isUserRegistered:
			if regRequest.status == 1:
				regRequest.message = "Your response has been saved."
			elif regRequest.status == 2:
				regRequest.message = "Your request to participate in this event is declined."
			elif regRequest.status == 3:
				regRequest.message = "Your request to participate in this event is approved."
			elif regRequest.status == 4:
				regRequest.message = "You have participated in this event."
			response['regRequest'] = regRequest
		return render(request,'events/registerEvent.djt',response)
	except:
		return redirect('/events')

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
def viewResponses(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		questions = EventQuestion.objects.filter(event = event)
		regRequests = EventRegisterationRequest.objects.filter(event = event)
		response['event'] = event
		response['questions'] = questions
		response['regRequests'] = regRequests
		return render(request,'events/eventResponse.djt',response)
	except:
		print("Error occured while managing event.")
	return redirect('/events')

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
@api_view(['GET','POST'])
def getResponse(request):
	data = {}
	if request.method == 'GET':
		data['dummy'] = "dummy date"

		# print stserial.data
		return Response(data)

	if request.method == 'POST' :
		print request.POST
		eventId =  request.POST['eventpk']
		username = request.POST['username']
		event = Event.objects.get(pk = eventId)
		print event
		user = User.objects.get(username = username)
		print user
		questions = EventQuestion.objects.filter(event = event)
		for question in questions:
			questionResponse = EventQuestionResponse.objects.get(question = question, user = user)
			res =  questionResponse.response
			data['ques%d'%question.pk] = res


		# print stserial.data
		return Response(data)

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
@api_view(['PUT'])
def updateRegRequest(request):
	data = {}
	if request.method == 'PUT' :
		print request.POST
		# print stserial.data
		requestId =  request.POST['requestId']
		status = request.POST['status']
		regRequest = EventRegisterationRequest.objects.get(pk = requestId)
		print regRequest
		regRequest.status = status
		regRequest.save()
		return Response(data)