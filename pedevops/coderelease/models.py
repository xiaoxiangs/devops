#/usr/bin/python
#coding: utf-8
from django.db import models
# Create your models here.

class program_name(models.Model):
    name = models.CharField(max_length=128)
    approval_user = models.CharField(max_length=64)
    approval_mail = models.CharField(max_length=128)
    test_host = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class release_status(models.Model):
    approval_user = models.CharField(max_length=64)
    release_version = models.CharField(max_length=128)
    release_user = models.CharField(max_length=64)
    release_time = models.CharField(max_length=64)
    release_status = models.PositiveSmallIntegerField(default=0)
    release_program = models.ForeignKey(program_name,default=1,related_name='program_name')

    def __unicode__(self):
        return '%s,%s,%s' % (self.release_program,self.release_version,self.release_status)


class release_diary(models.Model):
    diary_version = models.CharField(max_length=128)
    release_reader = models.CharField(max_length=64)
    follow_mail = models.CharField(max_length=128, null=True, blank=True)
    git_path = models.CharField(max_length=256)
    input_time = models.CharField(max_length=64, null=True, blank=True)
    approval_time = models.CharField(max_length=64, null=True, blank=True)
    release_time = models.CharField(max_length=64, null=True, blank=True)
    release_status = models.PositiveSmallIntegerField(default=0)
    remark = models.CharField(max_length=256,null=True, blank=True)
    release_program = models.ForeignKey(program_name,default=1,related_name='program_names')

    def __unicode__(self):
        return self.diary_version


class rollback_diary(models.Model):
    rollback_version = models.CharField(max_length=128)
    rollback_nextversion = models.CharField(max_length=128)
    rollback_time = models.CharField(max_length=64)
    rollback_mark = models.CharField(max_length=256,null=True, blank=True)
    rollback_status = models.PositiveSmallIntegerField(default=0)
    release_program = models.ForeignKey(program_name,default=1,related_name='program_namess')

    def __unicode__(self):
        return self.rollback_version

