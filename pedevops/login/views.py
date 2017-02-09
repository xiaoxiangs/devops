#!/usr/bin/python2.6
#coding: utf-8
import urllib
import httplib
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from models import Users,role,permission
from form import UserEditForm,RoleEditForm,PermissionlistForm
from django_page import django_Page
# Create your views here.

def test(request):
#    user = request.session.get('user')
#    if user:
    return render_to_response('login/test.html',{})
#    return render(request,'login/test.html',{})
#    else:
#        return HttpResponseRedirect('/login/')

def login_check(requestinfo):
    user = requestinfo.session.get('user')
    user_roleid = requestinfo.session.get('user_roleid')
    userinfo = {'user':user,'user_roleid':user_roleid}
    return userinfo

def PermissionVerify():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.session.get('user')
            if not user:
                return HttpResponseRedirect('/login')
            iUser = Users.objects.get(username=user)

            if iUser.role != 2:
                if not iUser.role:
                    return HttpResponseRedirect(reverse('permissiondeny'))
                role_permission = role.objects.get(name=iUser.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    if request.path == x.url: #or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)
                    else:
                        pass
                print '%s---->matchUrl:%s' %(user,str(matchUrl))
                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse('permissiondeny'))
            else:
                pass

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def permissiondeny(request):
    kwvars = {'request':request,}
    return render(request,'login/permission.not.html',kwvars)


def home(request):
    user = request.session.get('user')
    if user:
        kwvars = login_check(request)
        return render(request,'login/home.html',kwvars)
    else:
        return HttpResponseRedirect('/login/')

def login(request):
#    if request.method == 'GET' and request.GET.has_key('next'):
#        nexts = request.GET['next']
#    else:
#        nexts = '/loginss/'
    ticket= request.GET.get('ticket','')
    href=request.META['HTTP_HOST']
    if ticket:
        params = urllib.urlencode({'t': ticket,'d':1})
        headers = {"Referer ": "http://%s/" % href}
        conn = httplib.HTTPSConnection("passport.xxx.com")
        urll="/verify.php?%s" % params
        conn.request("GET", urll,'',headers)
        r1 = conn.getresponse()
        msg=r1.read()
        user = msg.split('@')[0]
        user_roleid = 3
        clientip = request.META['REMOTE_ADDR']
        times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            usermsg = Users.objects.get(email=msg)
            user_roleid = int(usermsg.role_id)
            usermsg.lastlogintime = times
            usermsg.lastloginip = clientip
            usermsg.save()
        except:
            usermsg = Users(username=user,password=msg,email=msg,lastlogintime=times,lastloginip=clientip,createtime=times,is_active=1,role_id=3)
            usermsg.save()

        request.session['user'] = user
        request.session['user_roleid'] = user_roleid
        return HttpResponseRedirect('/')
    return render(request,'login/login.rootpage.html',{})

def logout(request):
    try:
        del request.session['user']
        del request.session['user_roleid']
    except Exception,e:
        print e
    return render(request,'login/login.rootpage.html',{})

@PermissionVerify()
def userlist(request):
    kwvars = login_check(request)
    mlist = Users.objects.select_related().all()
    lst = django_Page(request,mlist,20)
    kwvars['IPage'] = lst
    print kwvars
    return render(request,'login/user.list.html',kwvars)


@PermissionVerify()
def userdelete(request,ID):
    kwvars = login_check(request)
    Users.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('userlist'))

@PermissionVerify()
def useredit(request,ID):
    kwvars = login_check(request)
    userinfo = Users.objects.get(id=ID)
    if request.method == 'POST':
        form = UserEditForm(request.POST,instance=userinfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('userlist'))
        else:
            return HttpResponse('error')
    else:
        form = UserEditForm(instance=userinfo)
    kwvars['form'] = form
    kwvars['ID'] = ID
    return render(request,'login/user.edit.html',kwvars)

@PermissionVerify()
def rolelist(request):
    kwvars = login_check(request)
    mlist = role.objects.select_related().all()
    lst = django_Page(request,mlist,20)
    kwvars['IPage'] = lst
    return render(request,'login/role.list.html',kwvars)

@PermissionVerify()
def roleedit(request,ID):
    kwvars = login_check(request)
    roleinfo = role.objects.get(id=ID)
    if request.method == 'POST':
        form = RoleEditForm(request.POST,instance=roleinfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rolelist'))
        else:
            return HttpResponse('error')
    else:
        form = RoleEditForm(instance=roleinfo)
    kwvars['form'] = form
    kwvars['ID'] = ID
    return render(request,'login/role.edit.html',kwvars)

@PermissionVerify()
def permissionlist(request):
    kwvars = login_check(request)
    mlist = permission.objects.select_related().all()
    lst = django_Page(request,mlist,20)
    kwvars['IPage'] = lst
    return render(request,'login/permission.list.html',kwvars)

@PermissionVerify()
def permissionadd(request):
    kwvars = login_check(request)
    if request.method == "POST":
        form = PermissionlistForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permissionlist'))
    else:
        form = PermissionlistForm()
        kwvars['form'] = form
        return render(request,'login/permission.add.html',kwvars)

@PermissionVerify()
def permissionedit(request,ID):
    kwvars = login_check(request)
    iPermission = permission.objects.get(id=ID)
    if request.method == "POST":
        form = PermissionlistForm(request.POST,instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permissionlist'))
    else:
        form = PermissionlistForm(instance=iPermission)
        kwvars['ID'] = ID
        kwvars['form'] = form
        return render(request,'login/permission.edit.html',kwvars)

@PermissionVerify()
def permissiondelete(request,ID):
    kwvars = login_check(request)
    permission.objects.filter(id = ID).delete()
    return HttpResponseRedirect(reverse('permissionlist'))
