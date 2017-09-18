# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 下午4:40'

from django.conf.urls import url
from .views import TopicCreateView, TopicDetailView, TopicUpdateView, TopicDeleteView
from .views import AddFavView, AddCommentView, RemoveCommentView, TopicTopView
from .views import UploadImageView

urlpatterns = [
    # 发布话题
    url(r'^create/$', TopicCreateView.as_view(), name='create'),
    # 话题内容
    url(r'^detail/(?P<topic_id>\d+)/$', TopicDetailView.as_view(), name='detail'),
    # 更新话题
    url(r'^update/(?P<topic_id>\d+)/$', TopicUpdateView.as_view(), name='update'),
    # 删除话题
    url(r'^delete/(?P<topic_id>\d+)/$', TopicDeleteView.as_view(), name='delete'),
    # 收藏话题
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    # 置顶话题
    url(r'^top/$', TopicTopView.as_view(), name="top"),
    # 添加评论or回复
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    # 屏蔽评论or回复
    url(r'^remove_comment/(?P<comm_id>\d+)/$', RemoveCommentView.as_view(), name="remove_comment"),
    # 上传图片
    url(r'^upload/$', UploadImageView.as_view(), name="upload"),
]
