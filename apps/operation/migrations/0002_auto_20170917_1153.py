# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-17 11:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('topics', '0001_initial'),
        ('operation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.Topic', verbose_name='\u8bc4\u8bba\u6240\u5c5e\u8bdd\u9898'),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]