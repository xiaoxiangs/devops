# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('permission', models.ManyToManyField(related_name='permissionlist', to='login.permission', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150, blank=True)),
                ('email', models.CharField(max_length=300, blank=True)),
                ('lastlogintime', models.CharField(max_length=64, null=True, blank=True)),
                ('lastloginip', models.CharField(max_length=75, blank=True)),
                ('createtime', models.CharField(max_length=64)),
                ('is_active', models.BooleanField(default=False)),
                ('role', models.ForeignKey(related_name='rolelist', blank=True, to='login.role', null=True)),
            ],
        ),
    ]
