# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from xlsxwriter.workbook import Workbook
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
		event.name = request.POST['name']
		event.description = request.POST['description']
		event.timings = request.POST['timings']
		event.venue = request.POST['venue']
		event.organiser = request.POST['organiser']
		event.cost = request.POST['cost']
		event.softreq = request.POST['softreq']
		if request.FILES.get('logo'):
			event.logo = request.FILES.get('logo')
		if request.FILES.get('banner_image'):
			event.banner_image = request.FILES.get('banner_image')
		event.startdate = datetime.strptime(request.POST['startDate'], '%Y-%m-%d')
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
		event.name = request.POST['name']
		event.description = request.POST['description']
		event.timings = request.POST['timings']
		event.venue = request.POST['venue']
		event.organiser = request.POST['organiser']
		event.cost = request.POST['cost']
		event.softreq = request.POST['softreq']
		event.startdate = datetime.strptime(request.POST['startDate'], '%Y-%m-%d')
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

		if request.FILES.get('logo'):
			event.logo = request.FILES.get('logo')
		if request.FILES.get('banner_image'):
			event.banner_image = request.FILES.get('banner_image')

		event.save()
		return redirect('/events/manageevent/%d'%event.pk)

	questions = EventQuestion.objects.filter(event = event)
	response['event'] = event
	response['questions'] = questions
	response['startdate'] = event.startdate.strftime("%Y-%m-%d")
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
	# try:
	event = Event.objects.get(id=id)
	# Displaying event only if event is published or the user is superuser
	if event.isPublished or request.user.is_superuser:
		if event.isEventEnded :
			eventReqUser = EventRegisterationRequest.objects.filter(event=event,status=4)
			title = "Participated Users"
			if event.contents.filter(title = title).count() == 0:
				print "new participation list"
				content = Content()
				content.title = title
				content.content = "<h5 class='headh3'>List of users participated</h5>\n<ol>"
				for regRequest in eventReqUser :
					content.content += "<li class='userList'><a href=/auth/profile/"+ regRequest.user.profile.regNum + ">" + regRequest.user.first_name + ' ' + regRequest.user.last_name + "</a></li>\n<br>"
				content.content += "</ol>"
				content.save()
				event.contents.add(content)
				event.save()
				
			else :
				print "old participation list"
				content = event.contents.get(title = title)
				content.content = "<h5 class='headh3'>List of Participants :-</h5>\n<ol>"
				for regRequest in eventReqUser :
					content.content += "<li class='userList'><a href=/auth/profile/"+ regRequest.user.profile.regNum + ">" + regRequest.user.first_name + ' ' + regRequest.user.last_name + "</a></li>\n<br>"
				content.content += "</ol>"
				content.save()
				event.contents.add(content)
				event.save()
				

		response['event'] = event
		if request.user.is_authenticated() and EventRegisterationRequest.objects.filter(event = event, user = request.user).count() > 0:
			regRequest = EventRegisterationRequest.objects.get(event = event, user = request.user)
			response['regRequest'] = regRequest
		return render(request,'events/EventPage.djt',response)
	else:
		raise
	# except:
	# 	return redirect('/events')

@login_required(login_url='/auth/login')
def registerEvent(request,id) :
	response= {}
	try:
		event = Event.objects.get(id=id)
		# Raising exception if event is not published or event has ended
		if not event.isPublished or event.isEventEnded:
			raise

		questions = EventQuestion.objects.filter(event = event)
		formOpen = False
		isUserRegistered = False
		# get registeration status if exist
		if EventRegisterationRequest.objects.filter(event = event, user = request.user).count() > 0:
			regRequest = EventRegisterationRequest.objects.get(event = event, user = request.user)
			isUserRegistered = True
			for question in questions:
				question.response = EventQuestionResponse.objects.get(question = question, user = request.user).response
		if event.isRegisterationOpen:
			formOpen = True
			if request.method == 'POST' :

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
							quesResponse.registerationRequest = regRequest
							quesResponse.question = question
							quesResponse.user = request.user
							quesResponse.response = question.response
							quesResponse.save()

						# Now user is registered for this event so changing the flag.
						isUserRegistered = True

					# response['message'] = "Response saved successfully."
				else:
					response['message'] = "Unable to save response"
		

		response['event'] = event
		response['questions'] = questions

		if isUserRegistered:
			if EventMessage.objects.filter(event=event, status=regRequest.status).count() == 0:
				eventMessage = EventMessage()
				eventMessage.status = regRequest.status
				eventMessage.event = event
				if eventMessage.status == 1:
					eventMessage.message = "Your registeration request has been Submitted."
				elif eventMessage.status == 2:
					eventMessage.message = "Your request to participate in the event is declined."
				elif eventMessage.status == 3:
					eventMessage.message = "Your request to participate in event is approved."
				elif eventMessage.status == 4:
					eventMessage.message = "You have participated in this event."

				eventMessage.save()
			else:
				status = regRequest.status
				eventMessage = EventMessage.objects.get(event=event, status=status)
				
			regRequest.message = eventMessage.message
			if (regRequest.status == 1 or regRequest.status == 2) and event.isRegisterationOpen == True:
				formOpen = True
			else:
				formOpen = False
			response['regRequest'] = regRequest

		#this flag is used to check if form should be displayed or not.
		if formOpen:
			response['formOpen'] = formOpen
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
		if questions.filter(question__icontains='team name').count() > 0:
			response['teamName'] = True
			teamNameQues = questions.get(question__icontains='team name')
			for regReq in regRequests:
				try:
					regReq.teamName = EventQuestionResponse.objects.get(question = teamNameQues, user = regReq.user).response
				except:
					regReq.teamName = None

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

@login_required(login_url='/auth/login')
@user_passes_test(checkuserifsuperuser, login_url='/auth/login')
def downloadResponses(request,id):
	print "export"
	event = Event.objects.get(id=id)
	questions = EventQuestion.objects.filter(event = event)
	regRequests = EventRegisterationRequest.objects.filter(event = event)

	response={}
	marksobj = []

	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename=' + event.name +'_responses.xlsx'
	book = Workbook(response, {'in_memory': True})
	sheet = book.add_worksheet('Sheet1')       
	bold = book.add_format({'bold': True, 'align':'center_across'})

	row_num = 0
	columns = [(u"Timestamp",20),(u"Reg No", 10),(u"Contact", 10),(u"First Name",15),(u"Last Name",15),(u"Course",10),(u"Status",10),]
	
	for question in questions:
		columns.append(tuple((question.question, 50)))

	for col_num in xrange(len(columns)):
		sheet.write(row_num, col_num, columns[col_num][0], bold)
		sheet.set_column(col_num, col_num, columns[col_num][1])

	for req in regRequests:
		# dataRow = [12, req.user.profile.regNum, req.user.first_name, req.user.last_name, req.user.profile.course, req.get_status_display]
		dataRow = [req.requestDate.strftime('%Y-%m-%d %H:%M:%S'), req.user.profile.regNum, req.user.profile.contact,req.user.first_name, req.user.last_name, req.user.profile.course, req.get_status_display()]
		for question in questions:
			questionResponse = EventQuestionResponse.objects.get(question = question, user = req.user)
			res =  questionResponse.response
			dataRow.append(res)
		row_num += 1
		for col_num in xrange(len(dataRow)) :
			sheet.write(row_num, col_num, dataRow[col_num])

	book.close()
	return response

def spura(request):
	response = {}
	return render(request,'events/spura.djt',response)


@login_required(login_url='/auth/login')
def registerspura(request):
	response = {}
	if request.method == 'POST' :
		try:
			awardResponse = AwardResponse.objects.get(user = request.user)
		except:
			awardResponse = AwardResponse()
			awardResponse.user = request.user
		awardResponse.stud1 = request.POST['stud1']
		awardResponse.stud2 = request.POST['stud2']
		awardResponse.stud3 = request.POST['stud3']
		awardResponse.stud4 = request.POST['stud4']
		awardResponse.titleofpaper = request.POST['titleofpaper']
		awardResponse.broadfield = request.POST['broadfield']
		awardResponse.abstract = request.POST['abstract']
		awardResponse.conclusion = request.POST['conclusion']
		awardResponse.googledoc = request.POST['googledoc']
		awardResponse.whyaward = request.POST['whyaward']
		awardResponse.suggestions = request.POST['suggestions']
		awardResponse.save()
	if AwardResponse.objects.filter(user = request.user).count() > 0:
		awardResponse = AwardResponse.objects.get(user = request.user)
		response['awardResponse'] = awardResponse
	return render(request,'events/spuraregister.djt',response)
