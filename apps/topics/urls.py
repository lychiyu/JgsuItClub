# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 下午4:40'

from django.conf.urls import url
from .views import TopicCreateView, TopicDetailView, TopicUpdateView, TopicDeleteView

urlpatterns = [
    # 发布话题
    url(r'^create/$', TopicCreateView.as_view(), name='create'),
    url(r'^detail/(?P<topic_id>\d+)$', TopicDetailView.as_view(), name='detail'),
    url(r'^update/(?P<topic_id>\d+)$', TopicUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<topic_id>\d+)$', TopicDeleteView.as_view(), name='delete'),
]
