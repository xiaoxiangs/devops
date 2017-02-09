#!/usr/bin/python
#coding: utf-8

from django import forms
from models import deletelogapply

class deletelogform(forms.Form):
    log_host = forms.CharField(label=u'日志主机',error_messages={'required':u'日志主机不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'必填,不可为空(hostname or ip)'}))
    log_path = forms.CharField(label=u'日志路径',max_length=255,initial='/data/logs',
        widget= forms.TextInput(attrs={'class':'form-control','placeholder':'默认为/data/logs'}))
    save_date = forms.CharField(label=u'保留天数',initial='7',
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'保留日志的天数,默认7天(必须为数字,否则按默认值处理)'}))
    mark = forms.CharField(label=u'备注',max_length=255,required=False,
        widget = forms.TextInput(attrs={'class':'form-control'}))


    def __init__(self,*args,**kwargs):
        super(deletelogform,self).__init__(*args,**kwargs)

class dns_updateform(forms.Form):
    operation_id = forms.CharField(label=u'操作类型',
        widget = forms.Select(choices=(('Add',u'添加'),('Modify',u'修改'),('Delete',u'删除'))))
    dns_name = forms.CharField(label=u'DNS名称',error_messages={'required':u'DNS名称不可为空'},
        widget = forms.TextInput(attrs={'placeholder':'必填,不可为空'}))
    domain = forms.CharField(label=u'操作域',
        widget = forms.Select(choices=(('',u'--------'),('d.xiaonei.com','d.xiaonei.com'))))
    record_type = forms.CharField(label=u'记录类型',
        widget = forms.Select(choices=(('A','A'),('CNAME','CNAME'))))
    analy_ip = forms.CharField(label=u'IP或CNAME地址',
        widget = forms.TextInput(attrs={'placeholder':'必填,不可为空'}))

    def __init__(self,*args,**kwargs):
        super(dns_updateform,self).__init__(*args,**kwargs)


class proxy_updateform(forms.Form):
    domain = forms.CharField(label=u'域名',error_messages={'required':u'域名不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'不可为空,多个请用,隔开'}))
    mapping_ip = forms.CharField(label=u'后端地址',error_messages={'required':u'后端地址,不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'不可为空,多个请用,隔开'}))
    mark = forms.CharField(label=u'操作说明',max_length=255,required=False,
        widget = forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self,*args,**kwargs):
        super(proxy_updateform,self).__init__(*args,**kwargs)


