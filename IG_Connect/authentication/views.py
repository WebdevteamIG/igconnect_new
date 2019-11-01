# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from projects.models import *
from updates.models import *
from .models import *
import random
import datetime

from django.core.mail import send_mail
import smtplib

def igconnect(request):
    response = {}
    news = NewsUpdate.objects.filter(isPublished=True)
    response['updates'] = news
    return render(request,'homepage.djt',response)

def home(request):
    response = {}
    return render(request,'test.djt',response)

def signin(request):
    if request.user.is_authenticated() and request.user.is_active == True :
        return redirect('/')
    if request.method == 'POST':
        user_name = request.POST['user_name']
        try:
            user = User._default_manager.get(username__iexact = user_name.lower())
            print user
            username = user.username
        except:
            print "username invalid"
            try:
                user = User.objects.filter(email = user_name).last()
                print user
                print user.username
                username = user.username
            except:
                print "Even email invalid"
                return render(request, 'authentication/login.djt', {'error' : 'User-Name/Password Invalid'})
        password = request.POST['password']
        print username
        user = authenticate(username = username, password = password)
        if user == None :
            return render(request, 'authentication/login.djt', {'error' : 'User-Name/Password Invalid'})
        elif user.is_active == False :
            login(request, user)
            return redirect('/auth/updateProfile')
        else : 
            login(request, user)
            return redirect('/')
    return render(request, 'authentication/login.djt', None)

def signout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.user.is_active == True:
        return redirect('/')
    if request.method == 'POST':
        regNum = request.POST['regNum']
        course = request.POST['course']
        branch = request.POST['branch']
        contact = request.POST['email']
        aboutMe = request.POST['about_me']
        profile_pic = request.FILES['profile_pic']
        resume = request.FILES['resume']
        user_ = Userprofile(user = request.user, regNum = regNum, course = course, branch = branch, contact = contact, aboutMe = aboutMe, profile_pic = profile_pic, resume = resume)
        if user_ == None :
            return render('authentication/register.djt', {'error' : "Authentication Error, Please Try Again."})
        user_.save()
        request.user.is_active = True
        request.user.save()
        return redirect('/')
    return render(request, 'authentication/register.djt', None)

def signup(request):
    if request.user.is_active == True and request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
	if Userprofile.objects.filter(regNum=request.POST['regNum']).count() > 0 :
            response = {}
            response['error'] = 'This Registration Number Has Already Been Registered'
            return render(request, 'authentication/signup.djt', response)
	
        username  = request.POST['username']
        emailadr  = request.POST['email']
        password  = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        if password != password2 :
            return render(request, 'authentication/signup.djt', {'error' : 'Passwords don\'t match'})
        try:
            user = User._default_manager.get(username__iexact = username.lower())
            return render(request, 'authentication/signup.djt', {'error':'User-Name Already Exists'})
        except User.DoesNotExist:
            user = User.objects.create_user(username = username, email = emailadr, first_name = first_name, last_name = last_name)
            user.set_password(password)
            user.save()
            profile = Userprofile()
            profile.user = user
            profile.regNum = request.POST['regNum']
            profile.save()
            user = authenticate(username = username, password = password)
            login(request, user)
            
            return redirect('/auth/updateProfile')
        # return redirect('/auth/login')
        
    return render(request, 'authentication/signup.djt', None)

def profile(request,regNum) :
    userProfile = Userprofile.objects.get(regNum=regNum)
    projects = Project.objects.filter(user=userProfile.user)
    events = ParticipatedEvent.objects.filter(user=userProfile.user)
    response = {}
    response['userProfile'] = userProfile
    response['projects'] = projects
    response['events'] = events
    return render(request,'authentication/profilepage.djt',response)

def forgotPassword(request) :
    response = {}
    if request.method == 'POST' :
        username = request.POST['username']
        try :
            user = User.objects.get(username=username)
            if user.email == request.POST['email'] : 
                rnum = random.randint(100000,999999)
                newpass = username+str(rnum)

                message = 'Hi, \n your new password is : '+ newpass
                sender = "ig-nitw@student.nitw.ac.in"
                receiver = user.email
                rlist = []
                rlist.append(receiver)
                try:
                    send_mail('IG Connect Account Password Reset',message,sender,rlist,fail_silently=False,)
                    user.set_password(newpass)
                    user.save()
                    return redirect('/auth/login')
                except :
                    response['error'] = 'Error resetting password , Sorry !!!'
            else : 
                response['error'] = 'Email doesn\'t Match with the registered email !!!'
        except Exception as e:
            response['error'] = '*** No such username ***'

    return render(request,'authentication/forgotPassword.djt',response)

def updateProfile(request) :
    response = {}
    if request.method == 'POST' :

        if Userprofile.objects.filter(regNum=request.POST['regNum']).count() > 0 and Userprofile.objects.get(regNum=request.POST['regNum']).user != request.user:
            response['error'] = 'The Registration Number( %s ) Has Already Been Registered' % request.POST['regNum']
            return render(request, 'authentication/updateProfile.djt', response)

        profile = Userprofile.objects.get(user=request.user)
        profile.regNum = request.POST['regNum']
        profile.course = request.POST['course']
        profile.branch = request.POST['branch']
        profile.contact = request.POST['contact']
        profile.aboutMe = request.POST['aboutMe']
        if request.FILES.get('profilepic') :
            profile.profile_pic = request.FILES.get('profilepic')
        if request.FILES.get('resume') :
            profile.resume = request.FILES.get('resume')
        profile.save()

        return redirect('/auth/profile/'+profile.regNum)
    return render(request,'authentication/updateProfile.djt',response)

def webteam(request) :
    response = {}
    return render(request,'webTeam.djt',response)

def contactUs(request) :
    response = {}
    if request.method == 'POST' :
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Content = 'Name : ' + name + '\n\n'
        Content = Content + 'Email : ' + email + '\n\n'
        Content = Content + 'Message : ' + message + '\n\n'
        
        receiver = "ig-nitw@student.nitw.ac.in"
        sender = "ig-nitw@student.nitw.ac.in"
        rlist = []
        rlist.append(receiver)
        try:
            send_mail('IG Connect Contact Us Message',Content,sender,rlist,fail_silently=False,)
            return redirect('/')
        except :
            print 'error sending message'
            response['error'] = 'Error sending Message , Sorry !!!'
    return redirect('/')
