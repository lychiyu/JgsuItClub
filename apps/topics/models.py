# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名')
    is_show = models.BooleanField(verbose_name='是否显示', default=True)

    class Meta:
        verbose_name = "话题分类"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name='话题标题')
    content = models.TextField(verbose_name='话题正文')
    is_top = models.BooleanField(default=False, verbose_name='话题是否置顶')
    is_show = models.BooleanField(default=True, verbose_name='话题是否显示')
    click_nums = models.IntegerField(default=0, verbose_name='浏览数')
    comment_nums = models.IntegerField(default=0, verbose_name='评论数')
    category = models.ForeignKey(Category, verbose_name='话题分类')
    author = models.ForeignKey(UserProfile, verbose_name='话题发布者')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')
    update_time = models.DateTimeField(default=datetime.now, verbose_name='最后一次修改时间')

    class Meta:
        verbose_name = "话题"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
