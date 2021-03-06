# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-17 11:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.IntegerField(default=0, verbose_name='\u8bc4\u8bba\u5b9e\u4f53\u7684id')),
                ('entity_type', models.IntegerField(choices=[(1, '\u8bc4\u8bba\u8bdd\u9898'), (2, '\u8bc4\u8bba\u7528\u6237\u8bc4\u8bba')], default=1, verbose_name='\u6536\u85cf\u7c7b\u578b')),
                ('comments', models.CharField(max_length=200, verbose_name='\u8bc4\u8bba')),
                ('comment_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='\u8bc4\u8bba\u70b9\u8d5e\u6570')),
                ('is_show', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a')),
            ],
            options={
                'verbose_name': '\u8bc4\u8bba\u7ba1\u7406',
                'verbose_name_plural': '\u8bc4\u8bba\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_id', models.IntegerField(default=0, verbose_name='\u8bdd\u9898id')),
                ('fav_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6536\u85cf\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6536\u85cf',
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_id', models.IntegerField(default=0, verbose_name='\u53d1\u9001\u7528\u6237id')),
                ('to_id', models.IntegerField(default=0, verbose_name='\u63a5\u6536\u7528\u6237id')),
                ('message', models.CharField(max_length=500, verbose_name='\u63a5\u6536\u7684\u6d88\u606f\u5185\u5bb9')),
                ('has_read', models.BooleanField(default=False, verbose_name='\u6d88\u606f\u662f\u5426\u5df2\u8bfb')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u9001\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6d88\u606f',
                'verbose_name_plural': '\u7528\u6237\u6d88\u606f',
            },
        ),
    ]
