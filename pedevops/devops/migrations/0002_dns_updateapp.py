# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dns_updateapp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dns_name', models.CharField(max_length=128)),
                ('domain', models.CharField(max_length=64)),
                ('record_type', models.CharField(max_length=8)),
                ('analy_ip', models.CharField(max_length=128)),
                ('update_ip', models.CharField(max_length=128, null=True, blank=True)),
                ('operation_id', models.CharField(max_length=32)),
                ('user', models.CharField(max_length=32)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('operation_date', models.CharField(max_length=32)),
                ('server_reqinfo', models.CharField(max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
