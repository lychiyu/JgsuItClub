# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 下午3:22'

import xadmin

from .models import Category, Topic


class CategoryAdmin(object):
    # 列表展示字段
    list_display = ['name', 'is_show']
    # 搜索字段
    search_fields = ['name', ]
    # 筛选字段
    list_filter = ['name', 'is_show']


class TopicAdmin(object):
    # 列表展示字段
    list_display = ['title', 'is_top', 'click_nums', 'comment_nums', 'category', 'author', 'create_time', 'update_time']
    # 搜索字段
    search_fields = ['title', 'is_top', 'click_nums', 'comment_nums', 'category', 'author']
    # 筛选字段
    list_filter = ['title', 'is_top', 'click_nums', 'comment_nums', 'category', 'author', 'create_time', 'update_time']


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Topic, TopicAdmin)
