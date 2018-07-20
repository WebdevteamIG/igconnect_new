# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import *

# Create your views here.

def index(request):
    experience = Experience.objects.order_by('projectName')
    ref_dict = {'name_ref':experience}
    return render(request,'experience/home.djt',context=ref_dict)

def add_exp(request):
    if request.method == 'POST':
        projectName = request.POST["projectName"]
        contributors = request.POST["contrib"]
        exp = request.POST["exp"]
        details = Experience(projectName=projectName, contributors=contributors, exp=exp)
        details.save()
        return redirect('/exp')

    return render(request,'experience/add_exp.djt')



