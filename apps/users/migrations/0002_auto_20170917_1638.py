# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-17 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='github',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Github\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='signature',
            field=models.CharField(blank=True, default='\u8fd9\u5bb6\u4f19\u5f88\u61d2\uff0c\u4ec0\u4e48\u4e2a\u6027\u7b7e\u540d\u90fd\u6ca1\u6709\u7559\u4e0b\u3002', max_length=200, null=True, verbose_name='\u4e2a\u6027\u7b7e\u540d'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weibo',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='\u5fae\u535a\u5730\u5740'),
        ),
    ]