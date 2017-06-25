# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from models import Userprofile

def index(request):
    if request.user.is_authenticated() and request.user.is_active == True :
        return redirect('/projects/')
    return redirect('/auth/login')

def login(request):
    if request.user.is_authenticated() and request.user.is_active == True :
        return redirect('/projects/')
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = reques.POST['password']
        user = authenticate(username = user_name, password = password)
        if user == None :
            return render(request, 'authentication/login.html', {'error' : 'User-Name/Password Invalid'})
        elif user.is_active == False :
            login(request, user)
            return redirect('/auth/register')
        else : 
            return redirect('/projects/')
    return render(request, 'authentication/login.html', None)

def logout(request):
    logout(request)
    return redirect('/auth/')

def register(request):
    if request.user.is_active == True:
        return redirect('/projects/')
    if request.method == 'POST':
        regNum = request.POST['reg_num']
        course = request.POST['course']
        branch = request.POST['branch']
        contact = request.POST['email']
        aboutMe = request.POST['about_me']
        profile_pic = request.FILES['profile_pic']
        resume = request.FILES['resume']
        user_ = Userprofile(user = request.user, regNum = regNum, course = course, branch = branch, contact = contact, aboutMe = aboutMe, profile_pic = profile_pic, resume = resume)
        if user_ == None :
            return render('authentication/register.html', {'error' : "Authentication Error, Please Try Again."})
        user_.save()
        request.user.is_active = True
        request.user.save()
        return redirect('/projects/')
    return render(request, 'authentication/register.html', None)

def signup(request):
    if request.user.is_active == True and request.user.is_authenticated():
        return redirect('/projects/')
    if request.method == 'POST':
        username  = request.POST['username'].lower()
        emailadr  = request.POST['email']
        password  = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name'] 
        if password != password2 :
            return render(request, 'authentication/signup.html', {'error' : 'Passwords don\'t match'})

        try:
            user = User._default_manager.get(username__iexact = username.lower())
            return render(request, 'authentication/signup.html', {'error':'User-Name Already Exists'})
        except User.DoesNotExist:
            user = User.objects.create_user(username = username, email = emailadr, first_name = first_name, last_name = first_name)
            user.set_password(password)
            user.is_active = False
            user.save()
        return redirect('/auth/register')
    return render(request, 'authentication/signup.html', None)