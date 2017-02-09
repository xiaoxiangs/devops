# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='deletelogapply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('log_host', models.CharField(max_length=128)),
                ('log_path', models.CharField(max_length=255)),
                ('save_date', models.PositiveSmallIntegerField()),
                ('mark', models.CharField(max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
