#!/usr/bin/python
#coding: utf-8
import os
import json
import datetime, time
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from form import deletelogform,dns_updateform,proxy_updateform
from devops_script import Deletelog
from models import deletelogapply,dns_updateapp,proxy_domain,proxy_update
from login.django_page import django_Page
from login.views import PermissionVerify,login_check
# Create your views here.


@PermissionVerify()
def deletelog(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
    if request.method == 'POST':
        form = deletelogform(request.POST)
        if form.is_valid():
            email = '%s@renren-inc.com' % kwvars['user']
            log_host = form.cleaned_data['log_host']
            log_path = form.cleaned_data['log_path']
            save_date = form.cleaned_data['save_date']
            try:
                cmd = 'rm %s' % log_path
                req = Deletelog.del_log(log_host,cmd,'deletelog')
            except Exception,e:
                reqs = '\n    %s' % e
                req = {'log_record':reqs,'code':1}
            else:
                mark = form.cleaned_data['mark']
                if req['code'] == 0:
                    status = 1
                else:
                    status = 2
                logdata = deletelogapply(username=kwvars['user'],email=email,log_host=log_host,log_path=log_path,save_date=save_date,mark=mark,status=status)
                logdata.save()
            my_json = json.dumps(req)
            return HttpResponse(my_json,content_type="application/json")
    else:
        form = deletelogform()
    kwvars['form'] = form
    return render(request,'devops/devops.deletelog.html',kwvars)
#    else:
#        return HttpResponseRedirect('/login')

def dns_updatetime():
    update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return update_time

@PermissionVerify()
def onlinestats(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
    if request.method == 'POST':
        strtime = request.POST['strdate']
        endtime = request.POST['endtate']
#            return HttpResponse(strtime)
    else:
        dates = datetime.datetime.now()
        endtime = dates.strftime('%Y-%m-%d')
        strtime = (dates - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    endtimes = '%s-23-59' % endtime
    strtimes = '%s-00-00' % strtime
    cmd = '/root/xiang.xiao3/dancer/project.py %s %s' % (strtimes,endtimes)
    proList = Deletelog.del_log('10.4.29.109',cmd,'onlinestats')
    proList = eval(proList['commd_out'])
    kwvars['strtime'] = strtime
    kwvars['endtime'] = endtime
    kwvars['proList'] = proList
    return render(request,'devops/devops.onlinestats.html',kwvars)
#    else:
#        return HttpResponseRedirect('/login')


@PermissionVerify()
def dns_check(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
#        kwvars = {'user':user,'user_roleid':user_roleid}
    if request.method == 'POST':
        dns_ip = request.POST['ip'].split(',')
        ip = {}
        for i in dns_ip:
            ip[i] = []
            dns_file = open('devops/devops_script/d.xiaonei.com','r')
            for d in dns_file.readlines():
                if i in d:
                    if i == d.split()[-1]:
                        dns_domain = '%s.d.xiaonei.com' % d.split()[0]
                        print dns_domain
                        ip[i].append(dns_domain)
            dns_file.close()
        if ip != {}:
            st_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.stat("devops/devops_script/d.xiaonei.com").st_mtime))
            kwvars['st_time'] = st_time
            kwvars['ip'] = ip
    return render(request,'devops/devops.dns_check.html',kwvars)
#    else:
#        return HttpResponseRedirect('/login')


@PermissionVerify()
def dns_update(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
#        kwvars = {'user':user,'user_roleid':user_roleid}
    if request.method == 'POST':
        req_dict = {}
        dns_name = request.POST.getlist('dns_name')
        domain = request.POST.getlist('domain')
        operation_id = request.POST.getlist('operation_id')
        record_type = request.POST.getlist('record_type')
        analy_ip = request.POST.getlist('analy_ip')
        for dom in dns_name:
            dom_index = dns_name.index(dom)
            if dom !='' and analy_ip[dom_index] != '':
                req_dom = 'req_%s' % dom_index
                req_dict[req_dom] = [operation_id[dom_index],dns_name[dom_index],domain[dom_index],record_type[dom_index],analy_ip[dom_index]]
            elif dom == '' and analy_ip[dom_index] == '':
                pass
            else:
                kwvars['updatereq'] = '您的输入有误,请检查DNS名称或IP地址输入是否正确.谢谢!'

        if len(req_dict) == 0 and len(kwvars) == 0:
            kwvars['updatereq'] = '请填写需要操作的DNS信息后提交.谢谢!'
        else:
            uptime = dns_updatetime()
            for db in req_dict.values():
                #dns_names = '%s.%s' % (db[1], db[2])
                dns_updateapp.objects.create(dns_name=db[1],domain=db[2],record_type=db[3],analy_ip=db[4],operation_id=db[0],user=kwvars['user'],operation_date=uptime,status=1)
                kwvars['updatereq'] = '提交成功,请等待管理员操作.谢谢!'
        return render(request,'devops/devops.dns_req.html',kwvars)
    if kwvars['user_roleid'] == 1:
        dnslist = dns_updateapp.objects.order_by('-id')[:100]
    else:
        dnslist = dns_updateapp.objects.filter(user = kwvars['user']).order_by('-id')
    form = dns_updateform()
    kwvars['form'] = form
    kwvars['ranges'] = range(1,4)
    kwvars['dnslist'] = dnslist
    return render(request,'devops/devops.dns_update.html',kwvars)
#else:
#        return HttpResponseRedirect('/login')

@PermissionVerify()
def dns_cancel(request,ID):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
#        kwvars = {'user':user,'user_roleid':user_roleid}
    if kwvars['user_roleid'] == 1:
        reqinfo = request.POST['reqinfo']
        stats = 5
    else:
        reqinfo = '用户取消'
        stats = 4
    uptime = dns_updatetime()
    dns_updateapp.objects.filter(id = ID).update(operation_date=uptime,status=stats,server_reqinfo=reqinfo)

    return HttpResponseRedirect(reverse('dns_update'))
#    else:
#        return HttpResponseRedirect('/login')


@PermissionVerify()
def dns_apply(request,ID):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
    if kwvars['user_roleid'] ==1:
        uptime = dns_updatetime()
        dns_updateapp.objects.filter(id = ID).update(operation_date=uptime,status = 2)

        return HttpResponseRedirect(reverse('dns_update'))
#    else:
#        return HttpResponseRedirect('/login')


@PermissionVerify()
def proxy_updates(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
#        kwvars = {'user':user,'user_roleid':user_roleid}
    if request.method == 'POST':
        if 'domain_check' in request.POST:
            domaincheck_list = request.POST['domain_check'].split(',')
            domaincheck = {}
            for i in domaincheck_list:
                domaininfo = proxy_domain.objects.filter(dns=i,mark='').values('ip','conf_id')
                print domaininfo
                domaindic,relationlist = {},[]
                if len(domaininfo) != 0:
                    domains = domaininfo[0]['ip'].split(',')
                    for d in domains:
                        domains[domains.index(d)] = d.split()[0]
                    relationid = int(domaininfo[0]['conf_id'])
                    print relationid
                    relation = proxy_domain.objects.filter(conf_id=relationid,mark='').values('dns')
                    for r in relation:
                        relationlist.append(r['dns'])
                    domaindic['ip'] = domains
                    domaindic['relation'] = relationlist
                domaincheck[i] = domaindic
            if domaincheck != {}:
                kwvars['domain_check'] = domaincheck
                print domaincheck
        else:
            form = proxy_updateform(request.POST)
            req = {'code':1}
            if form.is_valid():
                domain = form.cleaned_data['domain']
                mapping_ip = form.cleaned_data['mapping_ip']
                mark = form.cleaned_data['mark']
                operation_date = dns_updatetime()
                try:
                    proxy_update.objects.create(user=kwvars['user'],domain=domain,mapping_ip=mapping_ip,operation_date=operation_date,mark=mark,status=1)
                except Exception,e:
                    req['reqinfo'] = '\n    %s' % e
                else:
                    req['code'] = 0
                my_json = json.dumps(req)
                return HttpResponse(my_json,content_type="application/json")
    kwvars['form'] = proxy_updateform()
    return render(request,'devops/devops.proxy_update.html',kwvars)
#    else:
#        return HttpResponseRedirect('/login')

@PermissionVerify()
def proxy_updatelist(request):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
#        kwvars = {'user':user,'user_roleid':user_roleid}
    if kwvars['user_roleid'] == 1:
        mlist = proxy_update.objects.order_by('-id')[:100]
    else:
        mlist = proxy_update.objects.filter(user = kwvars['user']).order_by('-id')
    lst = django_Page(request,mlist,20)
    kwvars['IPage'] = lst
    print lst
    return render(request,'devops/devops.proxy_update_list.html',kwvars)
#    else:
#        return HttpResponseRedirect('/login')

@PermissionVerify()
def proxy_apply(request,ID):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
    proxy_update.objects.filter(id = ID).update(status = 2)
    return HttpResponseRedirect(reverse('proxy_updatelist'))
#    else:
#        return HttpResponseRedirect('/login')


@PermissionVerify()
def proxy_okapply(request,ID):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
    proxy_update.objects.filter(id = ID).update(status = 3)
    return HttpResponseRedirect(reverse('proxy_updatelist'))
#    else:
#        return HttpResponseRedirect('/login')

@PermissionVerify()
def proxy_cancel(request,ID):
    kwvars = login_check(request)
#    user = request.session.get('user')
#    if user:
#        user_roleid = request.session.get('user_roleid')
    if kwvars['user_roleid'] == 1:
        reqinfo = request.POST['reqinfo']
        stats = 5
    else:
        reqinfo = '用户取消'
        stats = 4
    uptime = dns_updatetime()
    proxy_update.objects.filter(id = ID).update(status=stats,reqinfo=reqinfo)

    return HttpResponseRedirect(reverse('proxy_updatelist'))
#    else:
#        return HttpResponseRedirect('/login')


