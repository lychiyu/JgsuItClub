# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile
from topics.models import Topic


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='话题id')
    fav_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    topic = models.ForeignKey(Topic, verbose_name='评论所属话题')
    entity_id = models.IntegerField(default=0, verbose_name='评论实体的id')
    entity_type = models.IntegerField(default=1, choices=((1, '评论话题'), (2, '评论用户评论')), verbose_name='收藏类型')
    comments = models.CharField(max_length=200, verbose_name='评论')
    comment_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')
    fav_nums = models.IntegerField(default=0, verbose_name='评论点赞数')
    is_show = models.BooleanField(default=True, verbose_name="是否显示")

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    from_id = models.IntegerField(default=0, verbose_name='发送用户id')
    to_id = models.IntegerField(default=0, verbose_name='接收用户id')
    message = models.CharField(max_length=500, verbose_name='接收的消息内容')
    has_read = models.BooleanField(default=False, verbose_name='消息是否已读')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name
