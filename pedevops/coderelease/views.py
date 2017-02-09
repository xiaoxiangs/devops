#!/usr/bin/python
#coding: utf-8
import datetime
from django.shortcuts import render
from login.django_page import django_Page
from django.core.urlresolvers import reverse
from login.views import PermissionVerify,login_check
from django.http import HttpResponse,HttpResponseRedirect
from forms import programaddform,releaseputform
from models import release_diary,release_status
# Create your views here.

def time_req():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def programadd(request):
    kwvars = login_check(request)
    if request.method == 'POST':
        form = programaddform(request.POST)
        if form.is_valid():
            print 'ttttttttttttttttt'
            form.save()
            return HttpResponseRedirect(reverse('coderelease_list'))
#        else:
            print form
    else:
        form = programaddform()
    kwvars['form'] = form

    return render(request,'coderelease/coderelease_list.html',kwvars)
