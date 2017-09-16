# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import Category, Topic
from utils.mixin_util import LoginRequiredMixin


class TopicCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'topic-edit.html', {})

    def post(self, request):
        cate = request.POST.get('category')
        title = request.POST.get('category')
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


class TopicDetailView(View):
    def get(self, request, topic_id):
        # 获取该话题
        topic = Topic.objects.get(id=topic_id)
        topic.click_nums += 1
        topic.save()

        # 作者其他话题
        user = topic.author
        other_topics = user.topic_set.filter(category__in=(1, 2))[:10]
        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, category__in=(1, 2))[:10]
        return render(request, 'topic-detail.html', {
            'topic': topic,
            'other_topics': other_topics,
            'no_comment_topics': no_comment_topics,
        })
