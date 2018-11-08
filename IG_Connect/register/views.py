# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
import requests

# Create your views here.

def index(request):
    response = {}
    if(request.method == "POST"):
        pay = Form()
        if(request.POST.get('yes', False) == "on"):
            pay.choice = True
        pay.title = request.POST["title"]
        pay.date = request.POST["date"]
        pay.save()
        response["choice"] = pay.choice
        response["title"] = pay.title
        if(pay.choice):
            return render(request, 'register/home.html', response)
    return render(request, 'register/home.html', response)

def register(request):
    response = {}
    form = Form.objects.all()
    response["form"] = form
    if(request.method == "POST"):
        reg = Registered()
        reg.title = Form.objects.get(title=request.POST["title"])
        reg.name = request.POST["name"]
        reg.year = request.POST["year"]
        reg.phone = request.POST["phone"]
        reg.email = request.POST["email"]
        reg.Regno = request.POST["regno"]
        reg.save()
        return redirect('/register/title')
    return render(request, 'register/form.html', response)

def send_info(request):
    msg= 'Company:' + name + '\nCTC:' + Ctc + '\nComment:' + comments 
    access_token = 'EAADfd1ZAZAWckBAHAjfGaSCT20sf95eqBeyVrbj9oA3CrUYdSuikPyDhenw9RTUEDjmtyFyn6C5EHgAjaxHjlYfohukza5WtmVmd8Gairg3D7Kvh8BIJyCfMNAANilsJhX4tI6rPzXhbifhYb63d6ZArX2yZADoG518B60p20gZDZD'
    access_token = 'access_token=' + access_token   