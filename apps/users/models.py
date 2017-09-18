# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    score = models.IntegerField(verbose_name='积分', default=0)
    weibo = models.CharField(max_length=200, verbose_name='微博地址', default='', blank=True, null=True)
    github = models.CharField(max_length=200, verbose_name='Github地址', default='', blank=True, null=True)
    signature = models.CharField(max_length=200, verbose_name='个性签名', default='这家伙很懒，什么个性签名都没有留下。', blank=True,
                                 null=True)
    image = models.CharField(max_length=200, verbose_name='用户头像的七牛云地址',
                             default='http://owcmz09se.bkt.clouddn.com/avatar.png')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nick_name

    def get_msg_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(to_id=int(self.id), has_read=False).count()


class EmailVerifyRecode(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='目标邮箱')
    send_type = models.CharField(max_length=12,
                                 choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')),
                                 verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


# 用户报名招新
class UserEnroll(models.Model):
    email = models.EmailField(max_length=100, verbose_name="邮箱")
    name = models.CharField(max_length=20, verbose_name="姓名")
    class_name = models.CharField(max_length=30, verbose_name="所在班级")
    qq = models.CharField(max_length=20, verbose_name="qq号码")
    phone = models.CharField(max_length=20, verbose_name="手机号码")
    reason = models.TextField(verbose_name="申请理由")
    status = models.CharField(max_length=1, default=0, verbose_name="审核状态",
                              choices=(('0', '未处理'), ('1', '未通过'), ('2', '已通过')))
    apply_time = models.DateTimeField(default=datetime.now, verbose_name='申请时间')

    class Meta:
        verbose_name = "用户招新报名"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取申请的用户
    def get_apply_user(self):
        return UserProfile.objects.get(email=self.email)
