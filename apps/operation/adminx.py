# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-17 上午9:11'

import xadmin

from .models import UserFavorite


class UserFavoriteAdmin(object):
    # 列表展示字段
    list_display = ['user', 'fav_id', 'fav_time']
    # 搜索字段
    search_fields = ['user', 'fav_id']
    # 筛选字段
    list_filter = ['user', 'fav_id', 'fav_time']


xadmin.site.register(UserFavorite, UserFavoriteAdmin)
