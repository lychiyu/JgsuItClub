# -*- coding: utf-8 -*-

import json
import uuid
import os
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.serializers import serialize
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Category, Topic
from operation.models import UserFavorite, UserComment, UserMessage

from utils.mixin_util import LoginRequiredMixin

from utils.qiniusdk import qiniu_upload_file
from config import DOMAIN_PREFIX
from JgsuItClub.settings import MEDIA_ROOT


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
        try:
            # 根据id获取话题
            topic = Topic.objects.get(id=topic_id, is_show=True)
        except Exception as e:
            topic = None

        if topic is not None:
            if curr_user.is_superuser or topic.author.id == curr_user.id:
                data = {"status": "0", 'title': topic.title, 'content': topic.content}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "1", "msg": "你不具备权限"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "1", "msg": "话题不存在"}), content_type='application/json')

    def post(self, request, topic_id):
        cate = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = Category.objects.get(name=cate)
        try:
            topic = Topic.objects.get(id=int(topic_id))
        except Exception as e:
            topic = topic()
        topic.title = title
        topic.content = content
        topic.category = category
        topic.author = request.user
        topic.author.save()
        topic.save()
        data = {"status": "0", "msg": topic.id}
        return HttpResponse(json.dumps(data), content_type='application/json')


class TopicDetailView(View):
    def get(self, request, topic_id):
        # 当前用户是否收藏了该话题
        has_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=topic_id)
            if user_fav:
                has_fav = True

        try:
            # 根据id获取话题
            topic = Topic.objects.get(id=topic_id, is_show=True)
        except Exception as e:
            topic = None
        if topic is not None:
            topic.click_nums += 1
            topic.save()
            # 作者其他话题
            user = topic.author
            other_topics = user.topic_set.filter(is_show=True, category__in=(1, 2))[:10]
            # 无人回复的话题
            no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2))[:10]

            all_comments = UserComment.objects.filter(topic=topic)
            return render(request, 'topic-detail.html', {
                'topic': topic,
                'other_topics': other_topics,
                'no_comment_topics': no_comment_topics,
                'all_comments': all_comments,
                'has_fav': has_fav,
            })
        else:
            return HttpResponseRedirect(reverse('index'))


class TopicDeleteView(LoginRequiredMixin, View):
    def post(self, request, topic_id):
        # 先获取当前用户，只有话题作者和超级用户可以删除话题
        curr_user = request.user
        try:
            # 根据id获取话题
            topic = Topic.objects.get(id=topic_id, is_show=True)
        except Exception as e:
            topic = None

        if topic is not None:
            if curr_user.is_superuser or topic.author.id == curr_user.id:
                topic.is_show = False
                topic.save()
                return HttpResponse(json.dumps({"status": "0", "msg": "删除成功"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "1", "msg": "你不具备权限"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "1", "msg": "话题不存在"}), content_type='application/json')


class AddFavView(LoginRequiredMixin, View):
    """
    用户收藏话题操作
    """

    def post(self, request):
        # 收藏的话题id
        fav_id = request.POST.get('fav_id', 0)
        # 判断是否已经收藏了,如果已经收藏了,就取消收藏
        exist_recodes = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id))
        if exist_recodes:
            # 取消收藏
            exist_recodes.delete()

            topic = Topic.objects.get(id=int(fav_id))
            topic.fav_nums -= 1
            if topic.fav_nums < 0:
                topic.fav_nums = 0
            topic.save()
            return HttpResponse('{"status":"0","msg":"收藏"}', content_type='application/json')
        else:
            if int(fav_id) > 0:
                user_fav = UserFavorite()
                user_fav.fav_id = int(fav_id)
                user_fav.user = request.user
                user_fav.save()
                topic = Topic.objects.get(id=int(fav_id))
                topic.fav_nums += 1
                topic.save()
                return HttpResponse('{"status":"0","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"1","msg":"收藏失败"}', content_type='application/json')


class TopicTopView(LoginRequiredMixin, View):
    """
    话题置顶操作
    """

    def post(self, request):
        if request.user.is_superuser:
            # 获取需要置顶的话题的id
            top_id = request.POST.get('top_id', 0)
            # 获取话题
            topic = Topic.objects.get(id=top_id)
            # 判断该话题是否已经处于置顶状态
            if topic.is_top:
                # 置顶状态，取消置顶
                topic.is_top = False
                topic.save()
                return HttpResponse('{"status":"0","msg":"置顶"}', content_type='application/json')
            else:
                # 未置顶状态，置顶
                topic.is_top = True
                topic.save()
                return HttpResponse('{"status":"0","msg":"已置顶"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"1","msg":"没有权限"}', content_type='application/json')


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        # 获取评论对象id,评论类型,评论内容
        topic_id = request.POST.get('topic_id')
        entity_id = request.POST.get('entity_id')
        entity_type = request.POST.get('entity_type')
        comments = request.POST.get('comments')
        # 根据topic_id获取评论的话题
        comment_topic = Topic.objects.get(id=int(topic_id))
        comment_entity = UserComment()

        comment_entity.user = request.user
        comment_entity.topic = comment_topic
        comment_entity.entity_id = entity_id
        comment_entity.entity_type = entity_type
        # 评论话题
        if entity_type == '1':
            comment_entity.comments = comments
            comment_entity.save()

            # 回复话题需要发生消息
            message = UserMessage()
            message.from_id = request.user.id
            message.to_id = comment_topic.author.id
            # 消息内容
            contents = '''<a href="/user/info/{0}" target="_blank">{1}</a>  回复了你的话题  <a href="/topic/detail/{2}#{3}" target="_blank">{4}</a>'''.format(
                request.user.id, request.user.nick_name, topic_id, comment_entity.id, comment_topic.title)

            message.message = contents
            message.save()

            # 评论用户的评论
        if entity_type == '2':
            # 获取评论用户评论 的那条评论
            to_comment = UserComment.objects.get(id=entity_id)
            # 然后在获取发布该条评论的用户
            to_user = to_comment.user
            # 拼接评论内容
            comments = '''[@{0}]({1}/user/info/{2})
{3}'''.format(to_user.nick_name, DOMAIN_PREFIX, to_user.id, comments)
            comment_entity.comments = comments
            comment_entity.save()

            # 回复评论需要发送消息
            message = UserMessage()
            message.from_id = request.user.id
            message.to_id = to_user.id
            # 消息内容
            contents = '''<a href="/user/info/{0}" target="_blank">{1}</a>  回复了你的评论  <a href="/topic/detail/{2}#{3}" target="_blank">{4}</a>'''.format(
                request.user.id, request.user.nick_name, topic_id, comment_entity.id, comment_topic.title)

            message.message = contents
            message.save()

        # 回复数需要加1
        comment_topic.comment_nums += 1
        comment_topic.save()
        # 用户回复积分+1
        comment_entity.user.score += 1
        comment_entity.user.save()
        return HttpResponse('{"status":"0","msg":"回复成功"}', content_type='application/json')


class RemoveCommentView(LoginRequiredMixin, View):
    def get(self, request, comm_id):
        # 只有超级用户可以屏蔽回复
        if request.user.is_superuser:
            # 根据主键来获取该条评论
            comment = UserComment.objects.get(id=int(comm_id))
            comment.is_show = False
            comment.comments = "该回复已被屏蔽"
            comment.save()
        return HttpResponseRedirect('/topic/detail/' + comm_id)


class UploadImageView(LoginRequiredMixin, View):
    """
    上传图片
    """

    def post(self, request):
        # 获取文件后先存在本地，再转存至七牛云
        file_obj = request.FILES.get('file', None)
        file_ext = ""
        if file_obj.name.rfind('.') > 0:
            file_ext = file_obj.name.rsplit('.', 1)[1].strip().lower()
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        path = default_storage.save('' + file_name, ContentFile(file_obj.read()))
        # 保存在本地的临时路径
        temp_file = os.path.join(MEDIA_ROOT, path)

        # 上传到七牛云 返回的是 七牛云上存储的地址
        image_url = qiniu_upload_file(file_name, temp_file)

        # 删除保存在本地的临时文件
        os.remove(temp_file)
        # 拼接成markdown的图片形式
        image_url = "\n![]({0})".format(image_url)
        data = {"status": "0", "msg": image_url}
        return HttpResponse(json.dumps(data), content_type='application/json')
