# -*- coding: utf8 -*-
"""JgsuItClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.views import RegisterView, LoginView, LogoutView, AciveUserView, IndexView
from users.views import ForgetPwdView, ResetPwdView, ModifyPwdView, MessageView, MessageReadView
from users.views import EnrollView, EnrollDetailView, EnrollListView
from django.views.static import serve
# from settings import STATIC_ROOT



import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<code>.*)/$', AciveUserView.as_view(), name='user_active'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<code>.*)/$', ResetPwdView.as_view(), name='user_active'),
    # 消息
    url(r'^message/$', MessageView.as_view(), name='message'),
    url(r'^read_msg/(?P<msg_id>\d+)/$', MessageReadView.as_view(), name='read_msg'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # 招新
    url(r'^enroll/$', EnrollView.as_view(), name="enroll"),
    # 申请详情
    url(r'^enroll/(?P<id>\d+)/$', EnrollDetailView.as_view(), name="enroll_detail"),
    url(r'^enroll_list/$', EnrollListView.as_view(), name="enroll_list"),
    url(r'^topic/', include('topics.urls', namespace='topic')),
    url(r'^user/', include('users.urls', namespace='user')),
    # 配置static,解决debug为false时static路径设置无效
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]


# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'