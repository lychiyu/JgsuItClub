# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-17 下午2:13'

from django.conf.urls import url
from .views import UserSettingView, UserResetPwdView, UploadImage, UserInfoView
from .views import UserTopicsView, UserFavTopicsView, UserSetSuperView

urlpatterns = [
    # 发布话题
    url(r'^setting/$', UserSettingView.as_view(), name='setting'),
    url(r'^resetpwd/$', UserResetPwdView.as_view(), name='resetpwd'),
    # 上传文件
    url(r'^upload/$', UploadImage.as_view(), name='upload'),
    # 用户信息
    url(r'^info/(?P<user_id>\d+)/$', UserInfoView.as_view(), name='info'),
    # 用户发表的话题
    url(r'^topic_list/(?P<user_id>\d+)/$', UserTopicsView.as_view(), name='topic_list'),
    # 用户收藏的话题
    url(r'^fav_list/(?P<user_id>\d+)/$', UserFavTopicsView.as_view(), name='fav_list'),
    # 设置为超级管理员
    url(r'^set_super/(?P<user_id>\d+)/$', UserSetSuperView.as_view(), name='set_super'),
    # 话题内容
    # url(r'^detail/(?P<topic_id>\d+)$', TopicDetailView.as_view(), name='detail'),
]
