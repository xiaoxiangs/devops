#!/usr/bin/python
#coding: utf-8
from django.db import models

# Create your models here.

class deletelogapply(models.Model):
    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    log_host = models.CharField(max_length=128)
    log_path = models.CharField(max_length=255)
    save_date = models.PositiveSmallIntegerField()
    mark = models.CharField(max_length=255,null=True)
    status = models.PositiveSmallIntegerField()

class dns_updateapp(models.Model):
    dns_name = models.CharField(max_length=128)
    domain = models.CharField(max_length=64)
    record_type = models.CharField(max_length=8)
    analy_ip = models.CharField(max_length=128)
    update_ip = models.CharField(max_length=128,null=True,blank=True)
    operation_id = models.CharField(max_length=32)
    user = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    operation_date = models.CharField(max_length=32)
    server_reqinfo = models.CharField(max_length=255,null=True)
    status = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.dns_name

class proxy_conf(models.Model):
    conf_file = models.CharField(max_length=128)

class proxy_domain(models.Model):
    dns = models.CharField(max_length=128)
    ip = models.CharField(max_length=255)
    modify_date = models.DateTimeField(auto_now_add=True)
    rollback = models.CharField(max_length=255,null=True,blank=True)
    mark = models.CharField(max_length=32,null=True)
    conf = models.ForeignKey(proxy_conf,related_name='proxyconf')

class proxy_update(models.Model):
    user = models.CharField(max_length=32)
    domain = models.CharField(max_length=128)
    mapping_ip = models.CharField(max_length=128)
    operation_date = models.CharField(max_length=32)
    reqinfo = models.CharField(max_length=32,null=True,blank=True)
    mark = models.CharField(max_length=255,null=True,blank=True)
    status = models.PositiveSmallIntegerField()
