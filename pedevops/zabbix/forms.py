#!/usr/bin/python
#coding: utf-8

from django import forms



class monitoruseredit(forms.Form):

    alias = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget = forms.TextInput(attrs={'class':'form-control'}))


    def __init__(self,*args,**kwargs):
        super(monitoruseredit,self).__init__(*args,**kwargs)


