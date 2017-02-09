#!/usr/bin/python
#coding: utf-8

from django import forms
from models import Users,role,permission

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username','role','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'role' : forms.Select(choices=[(x.name,x.name) for x in role.objects.all()],attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(UserEditForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'

class RoleEditForm(forms.ModelForm):
    class Meta:
        model = role
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'permission' : forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
        }
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(RoleEditForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['permission'].label=u'URL'
        self.fields['permission'].required=False


class PermissionlistForm(forms.ModelForm):
    class Meta:
        model = permission
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'url' : forms.TextInput(attrs={'class':'form-control'}),
        }
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(PermissionlistForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['url'].label=u'URL'
        self.fields['url'].error_messages={'required':u'请输入URL'}
