# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-17 下午2:13'

from django.conf.urls import url
from .views import UserSettingView, UserResetPwdView, UploadImage

urlpatterns = [
    # 发布话题
    url(r'^setting/$', UserSettingView.as_view(), name='setting'),
    url(r'^resetpwd/$', UserResetPwdView.as_view(), name='resetpwd'),
    # 上传文件
    url(r'^upload/$', UploadImage.as_view(), name='upload'),
    # 话题内容
    # url(r'^detail/(?P<topic_id>\d+)$', TopicDetailView.as_view(), name='detail'),
]
