# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devops', '0002_dns_updateapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='proxy_conf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conf_file', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='proxy_domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dns', models.CharField(max_length=128)),
                ('ip', models.CharField(max_length=255)),
                ('modify_date', models.DateTimeField(auto_now_add=True)),
                ('rollback', models.CharField(max_length=255, null=True, blank=True)),
                ('mark', models.CharField(max_length=32, null=True)),
                ('conf', models.ForeignKey(related_name='proxyconf', to='devops.proxy_conf')),
            ],
        ),
        migrations.CreateModel(
            name='proxy_update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('domain', models.CharField(max_length=128)),
                ('mapping_ip', models.CharField(max_length=128)),
                ('operation_date', models.CharField(max_length=32)),
                ('reqinfo', models.CharField(max_length=32, null=True, blank=True)),
                ('mark', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
