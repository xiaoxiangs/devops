#!/usr/bin/python
#coding: utf-8

from django import forms
from models import program_name,release_diary


class programaddform(forms.ModelForm):
    name = forms.CharField(label=u'项目名称',error_messages={'required':u'不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control'}))
    approval_user = forms.CharField(label=u'审批人',max_length=64,error_messages={'required':u'不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control'}))
    approval_mail = forms.CharField(label=u'联系邮箱',max_length=64,error_messages={'required':u'不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'多个请用,隔开'}))
    test_host = forms.CharField(label=u'预上线主机',error_messages={'required':u'不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = program_name
        fields = '__all__'
#        widgets = {
#            'name' : forms.TextInput(attrs={'class':'form-control'}),
#            'approval_user' : forms.TextInput(attrs={'class':'form-control'}),
#            'approval_mail' : forms.TextInput(attrs={'class':'form-control','placeholder':'多个请用,隔开'}),
#            'test_host' : forms.TextInput(attrs={'class':'form-control'}),
#        }

    def __init__(self,*args,**kwargs):
        super(programaddform,self).__init__(*args,**kwargs)

#        self.fields['name'].label=u'项目名称'
#        self.fields['name'].error_messages={'required':u'不可为空'}
#        self.fields['approval_user'].label= u'审批人'
#        self.fields['approval_user'].error_messages= {'required':u'不可为空'}
#        self.fields['approval_mail'].label= u'联系邮箱'
#        self.fields['approval_mail'].error_messages={'required':u'不可为空'}
#        self.fields['test_host'].label= u'预上线主机'
#        self.fields['test_host'].error_messages={'required':u'不可为空'}

    def clean(self):
        cleaned_data = super(programaddform, self).clean()
        appmail = cleaned_data.get('approval_mail')
        appuser = cleaned_data.get('approval_user') 
        if 'renren-inc.com' not in appmail:
            raise forms.ValidationError(u'邮箱输入错误')
#        if appmail == 'xiang.xiao3@renren-inc.com':
#            raise forms.ValidationError('邮箱输入重复')

        return appmail








class releaseputform(forms.Form):
    program = forms.CharField(label=u'更新项目',widget = forms.Select(choices=[(x.name,x.name) for x in program_name.objects.all()],attrs={'class':'form-control'}),)
    release_version = forms.CharField(label=u'更新版本',error_messages={'required':u'不可为空'},
        widget = forms.TextInput(attrs={'class':'form-control'}))
    git_path = forms.CharField(label=u'代码路径',error_messages={'required':u'不可为空'},
        widget = forms.Textarea(attrs={'class':'form-control','rows':'2'}))
    follow_user = forms.CharField(label=u'抄送邮箱',
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'多个请用,隔开'}))

    remark = forms.CharField(label=u'更新说明',error_messages={'required':u'不可为空'},
        widget = forms.Textarea(attrs={'class':'form-control','rows':'3'}))

    def __init__(self,*args,**kwargs):
        super(releaseputform,self).__init__(*args,**kwargs)

#    class Meta:
#        model = release_diary
#        fields = ('release_version','git_path','remark')

