# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import Category, Topic
from utils.mixin_util import LoginRequiredMixin


class TopicCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # 如果有id请求参数，就是修改话题,直接跳到修改页面通过起ajax请求update
        if request.GET.get('id'):
            return render(request, 'topic-update.html', {'id': request.GET.get('id')})
        return render(request, 'topic-edit.html')

    def post(self, request):
        cate = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = Category.objects.get(name=cate)
        topic = Topic()
        topic.title = title
        topic.content = content
        topic.category = category
        topic.author = request.user
        # 发布话题积分加5
        topic.author.score += 5
        topic.author.save()
        topic.save()
        data = {"status": "0", "msg": topic.id}
        return HttpResponse(json.dumps(data), content_type='application/json')


class TopicUpdateView(LoginRequiredMixin, View):
    def get(self, request, topic_id):
        # 先获取当前用户，只有话题作者和超级用户可以编辑话题
        curr_user = request.user
        # 根据id获取话题
        topic = Topic.objects.get(id=topic_id, is_show=True)

        if topic is not None:
            if curr_user.is_superuser or topic.author.id == curr_user.id:
                data = {"status": "0", 'title': topic.title, 'content': topic.content}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                return HttpResponse({"status": "1", "msg": "你不具备权限"}, content_type='application/json')
        else:
            return HttpResponse({"status": "1", "msg": "话题不存在"}, content_type='application/json')


class TopicDetailView(View):
    def get(self, request, topic_id):
        # 获取该话题
        topic = Topic.objects.get(id=topic_id, is_show=True)
        topic.click_nums += 1
        topic.save()
        # 作者其他话题
        user = topic.author
        other_topics = user.topic_set.filter(is_show=True, category__in=(1, 2))[:10]
        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2))[:10]
        return render(request, 'topic-detail.html', {
            'topic': topic,
            'other_topics': other_topics,
            'no_comment_topics': no_comment_topics,
        })


class TopicDeleteView(LoginRequiredMixin, View):
    def get(self, request, topic_id):
        # 先获取当前用户，只有话题作者和超级用户可以删除话题
        curr_user = request.user
        # 根据id获取话题
        topic = Topic.objects.get(id=topic_id, is_show=True)
        if topic is not None:
            if curr_user.is_superuser or topic.author.id == curr_user.id:
                topic.is_show = False
                topic.save()
                return HttpResponse({"status": "0", "msg": "删除成功"}, content_type='application/json')
            else:
                return HttpResponse({"status": "1", "msg": "你不具备权限"}, content_type='application/json')
        else:
            return HttpResponse({"status": "1", "msg": "话题不存在"}, content_type='application/json')
