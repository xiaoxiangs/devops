#!/usr/bin/python
#coding: utf-8
from scripts import api_authcheck
from django.shortcuts import render
from login.django_page import django_Page
from django.core.urlresolvers import reverse
from login.views import PermissionVerify,login_check
from django.http import HttpResponse,HttpResponseRedirect
from forms import monitoruseredit
# Create your views here.


def info_form(info,types=''):
    lists = ''
    for lis in info:
        if lists == '':
            lists = lis[types]
        else:
            lists += ',%s' % lis[types]
    return lists


@PermissionVerify()
def list(request,ID):
    kwvars = login_check(request)
#    userroleid = kwvars['user_roleid']
    hostlist,hostgroup = [], {}
#    if userroleid == 1:
    method='hostgroup.get'
    params={"output":['groupid','name']}
    hostgrouplist = api_authcheck.token(method,params).result_data()
    for i in hostgrouplist['result']:
        hostgroup[i['name']] = i['groupid']
    kwvars['hostgroupdic'] = hostgroup

    method='host.get'
    params={"output":['hostid','name','available',"snmp_available","jmx_available","ipmi_available","status"],'selectTriggers':['description','priority'],'selectGroups':['name'],'selectInterfaces':['interfaces','ip'],'selectParentTemplates':["templateid","name"]}

    if ID != '0':
        params['groupids'] = '%s' % ID
    hostinfo = api_authcheck.token(method,params)
    hostinfos = hostinfo.result_data()['result']
    for s in hostinfos:
        new_hostdic,new_avail,new_triggers = {},[],[]
        if s['available'] == '1':
            new_avail.append('ZBX')
        if s['snmp_available'] == '1':
            new_avail.append('SNMP')
        if s['jmx_available'] == '1':
            new_avail.append('JMX')
        if s['ipmi_available'] == '1':
            new_avail.append('IPMI')
        if new_avail == []:
            new_avail.append('Discovery')
        trigger = s['triggers']
        for t in trigger:
            tr = {}
            priority = t['priority']
            description = t['description']
            if priority == '2':
                tr[description] = 'Warning'
            elif priority == '3':
                tr[description] = 'Average'
            elif priority == '4':
                tr[description] = 'High'
            elif priority == '5':
                tr[description] = 'Disaster'
            if tr not in new_triggers: 
                new_triggers.append(tr)
        new_hostdic['hostid'] = s['hostid']
        new_hostdic['name'] = s['name']
        new_hostdic["status"] = s["status"]
        new_hostdic['available'] = new_avail
        new_hostdic['parentTemplates'] = info_form(s['parentTemplates'],'name')
        new_hostdic['interfaces'] = info_form(s['interfaces'],'ip')
        new_hostdic['groups'] = info_form(s['groups'],'name')
        new_hostdic['triggers'] = new_triggers
        hostlist.append(new_hostdic)
#    print hostlist
    lst = django_Page(request,hostlist,50)
    kwvars['IPage'] = lst
#    print request.path
    return render(request,'zabbix/monitor_list.html',kwvars)


@PermissionVerify()
def operation(request,groupid,hostid):
    kwvars = login_check(request)
#    userroleid = kwvars['user_roleid']
    host_status = request.GET.get('status')
    host_del = request.GET.get('operation')
#    if userroleid == 1:
    res_path = request.path.split('/')
    res_paths = '/'.join(res_path[:4])
    if host_status != None:
        host_method = 'host.update'
        host_params = {"hostid": hostid,'status' :host_status}
    if host_del != None:
        host_method = 'host.delete'
        host_params = []
        host_params.append(hostid)
    api_authcheck.token(host_method,host_params).result_data()
    return HttpResponseRedirect(res_paths)

@PermissionVerify()
def userlist(request,sID):
    kwvars = login_check(request)
#    userroleid = kwvars['user_roleid']
#    if userroleid == 1:
    groupmethod='usergroup.get'
    groupparams={"output":['usrgrpid','name']}
    usergrouplist = api_authcheck.token(groupmethod,groupparams).result_data()
    kwvars['usergrouplist'] = usergrouplist['result']

    usermethod='user.get'
    userparams={"output":['userid','alias','permission','type'],'selectMedias':['sendto','period'],'selectUsrgrps':['name','users_status'],'sortfield':'userid'}

    if sID != '0':
        userparams['usrgrpids'] = '%s' % sID

    userinfo = api_authcheck.token(usermethod,userparams)
    userinfolist = userinfo.result_data()['result']

    print userinfolist
    lst = django_Page(request,userinfolist,50)
    kwvars['IPage'] = lst

    return render(request,'zabbix/user_list.html',kwvars)

def userdel(request,usergroupid,userid):
    return HttpResponse('test') 


def api_check(method,params):
    req_info = api_authcheck.token(method,params)
    req_data = req_info.result_data()['result']
    return req_data

def monitoruseredit(request,userID):
    kwvars = login_check(request)
    monitormethod='user.get'
    monitorparams = {"output":['userid','alias','permission','type'],'userids':userID,'selectMedias':['sendto','period','mediatypeid'],'selectUsrgrps':['name','users_status'],'sortfield':'userid'} 
    monitoredituser = api_check(monitormethod,monitorparams)[0]

    ###mail && mobile
    user_conn = {}
    user_connect = monitoredituser['medias']
    for m in user_connect:
        if 'renren-inc.com' in m['sendto']:
            user_conn['sendEmail'] = m
        elif len(m['sendto']) == 11:
            user_conn['sendSms'] = m
    monitoredituser['medias'] = user_conn

    req_path = request.GET.get('next')
    if request.method == 'POST':
        usergroup = request.POST.getlist('usergroup')
        sendEmail = request.POST['sendEmail']
        sendSms = request.POST['sendSms']
        monitoruser = request.POST['monitoruser']

        user_grouplist = []
        for u in monitoredituser['usrgrps']:
            user_grouplist.append(u['usrgrpid'])

        if user_grouplist != usergroup:
            userupdatemethod='user.update'
            userupdateparams = {"userid":userID,"alias":monitoruser,"usrgrps":usergroup}
            api_check(userupdatemethod,userupdateparams)

        mediainfo = monitoredituser['medias']

        mails,smss = '',''
        if sendSms != '':
            if 'sendSms' in mediainfo:
                sms_id = mediainfo['sendSms']['mediatypeid']
            else:
                mediasmsmethod='mediatype.get'
                mediasmsparams={"output":["meidatypeid"],'filter':{'description':'sendSms'}}
                sms_id = api_check(mediasmsmethod,mediasmsparams)[0]['mediatypeid']
            smss = {"mediatypeid": sms_id, "sendto": sendSms, "active": 0,"severity": 63,"period": "1-7,00:00-24:00"}

        if sendEmail != '':
            if 'sendEmail' in mediainfo:
                mail_id = mediainfo['sendEmail']['mediatypeid']
            else:
                mediamailmethod='mediatype.get'
                mediamailparams={"output":["meidatypeid"],'filter':{'description':'sendEmail'}}
                mail_id = api_check(mediamailmethod,mediamailparams)[0]['mediatypeid']
            mails = {"mediatypeid": mail_id, "sendto": sendEmail, "active": 0,"severity": 63,"period": "1-7,00:00-24:00"}

        mediaupdatemethod = 'user.updatemedia'
        mediaupdateparams = {"users":{"userid": userID},"medias":[]}
        if mails == '' and smss == '':
            pass
        else:
            if mails != '':
                mediaupdateparams['medias'].append(mails)
            if smss != '':
                mediaupdateparams['medias'].append(smss)
        api_check(mediaupdatemethod,mediaupdateparams)

        return HttpResponseRedirect(req_path)

    usergroupmethod = 'usergroup.get'
    usergroupparams = {'output':['usrgrpid','name','users_status']}
    
    usergrouplist = api_check(usergroupmethod,usergroupparams)
    new_grouplist = []
    for g in  usergrouplist:
        if g not in monitoredituser['usrgrps']:
            new_grouplist.append(g)

    kwvars['edituser'] = monitoredituser
    kwvars['totaluser'] = new_grouplist
    kwvars['userID'] = userID
    kwvars['req_path'] = req_path

    return render(request,'zabbix/user_edit.html',kwvars)

def useradd(request):
    return HttpResponse('test')
