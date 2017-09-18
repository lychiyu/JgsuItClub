# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 下午3:13'

import xadmin
from xadmin import views
from .models import EmailVerifyRecode, UserEnroll


# xadmin全局设置
class GlobalSetting(object):
    site_title = '技术交流社区后台管理'
    site_footer = '技术交流社区'
    menu_style = 'accordion'


class EmailVerifyRecodeAdmin(object):
    # 列表展示字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索字段
    search_fields = ['code', 'email', 'send_type']
    # 筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


class UserEnrollAdmin(object):
    # 列表展示字段
    list_display = ['email', 'name', 'class_name', 'qq', 'phone', 'status', 'apply_time']
    # 搜索字段
    search_fields = ['email', 'name', 'class_name', 'qq', 'phone', 'status']
    # 筛选字段
    list_filter = ['email', 'name', 'class_name', 'qq', 'phone', 'apply_time']


xadmin.site.register(EmailVerifyRecode, EmailVerifyRecodeAdmin)
xadmin.site.register(UserEnroll, UserEnrollAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
