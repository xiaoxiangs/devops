from django.db import models
#coding:utf-8
# Create your models here.


class permission(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.url)

class role(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(permission,blank=True,related_name='permissionlist')

    def __unicode__(self):
        return self.name

class Users(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=300, blank=True)
    lastlogintime = models.CharField(max_length=64, null=True, blank=True)
    lastloginip = models.CharField(max_length=75, blank=True)
    createtime = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    role = models.ForeignKey(role,related_name='rolelist',default=3)

    def __unicode__(self):
        return self.username
#    class Meta:
#        db_table = u'user'
