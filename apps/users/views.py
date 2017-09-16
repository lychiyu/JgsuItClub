# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import UserProfile


# 自定义用户登录的逻辑
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
