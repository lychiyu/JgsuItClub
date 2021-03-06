# -*- coding:utf-8 -*-
import os
import json
import uuid

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response

from JgsuItClub.settings import MEDIA_ROOT

from config import DOMAIN_PREFIX

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from users.models import UserProfile, EmailVerifyRecode, UserEnroll
from users.forms import RegisterForm, LoginForm, ForgetPwdForm, ModifyPwdForm
from utils.email_send import send_email
from topics.models import Topic, Category
from utils.mixin_util import LoginRequiredMixin
from utils.qiniusdk import qiniu_upload_file
from operation.models import UserFavorite, UserMessage


# 自定义用户登录的逻辑
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 获取主机信息用于发送激活链接
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"status":"1","msg":"邮箱已经被注册了"}', content_type='application/json')
            nick_name = request.POST.get('nick_name', '')
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.nick_name = nick_name
            user_profile.email = email
            user_profile.username = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_email(email, DOMAIN_PREFIX)
            return HttpResponse('{"status":"0","msg":"欢迎您的注册，请您去邮箱中激活您的账号"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(register_form.errors), content_type='application/json')


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取邮箱和密码
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = UserProfile.objects.get(email=email)
            if user.is_active == 0:
                return HttpResponse('{"status":"1","msg":"账号尚未激活"}', content_type='application/json')
            # 验证用户
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                # return HttpResponseRedirect(reverse('index'))
                return HttpResponse('{"status":"0","msg":"登录成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"1","msg":"邮箱或密码错误"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"1","msg":"输入不合法"}', content_type='application/json')


class LogoutView(View):
    """
    退出登录
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class AciveUserView(View):
    def get(self, request, code):
        # 根据激活码获取记录
        all_recodes = EmailVerifyRecode.objects.filter(code=code)
        if all_recodes:
            for recode in all_recodes:
                email = recode.email
                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()
        else:
            return render(request, 'skip.html', {
                'title': '激活失败',
                'msg': '激活失败',
            })
        return HttpResponseRedirect(reverse('login'))


class IndexView(View):
    def get(self, request):
        # 获取keywords
        keywords = request.GET.get('keywords', '')

        # 获取cate参数
        cate_id = request.GET.get('cate', '0')
        if cate_id == 0:
            # 获取所有话题
            topics = Topic.objects.filter(is_show=True, category__in=(1, 2)).order_by('-is_top', '-create_time')
        else:
            try:
                category = Category.objects.get(id=int(cate_id))
                # 获取对应话题
                topics = Topic.objects.filter(is_show=True, category=category).order_by('-is_top', '-create_time')
            except Exception as e:
                cate_id = '0'
                topics = Topic.objects.filter(is_show=True, category__in=(1, 2))

        if keywords:
            topics = topics.filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(topics, 12, request=request)
        page_topics = p.page(page)

        # 获取所有话题分类
        cates = Category.objects.all()
        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2)).order_by('-is_top',
                                                                                                             '-create_time')[
                            :10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]

        # 是否打开招新功能
        apply_cate = Category.objects.get(id=4)

        return render(request, 'index.html', {
            'cates': cates,
            'topics': page_topics,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users,
            'cate_id': cate_id,
            'apply_cate': apply_cate,
        })


class UserSettingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'seeting.html', {'userprofile': request.user})

    def post(self, request):
        """
        用户修改个人信息
        :param request:
        :return:
        """
        nick_name = request.POST.get('nick_name', str(uuid.uuid1())[:8])
        weibo = request.POST.get('weibo', '')
        github = request.POST.get('github', '')
        signature = request.POST.get('signature', '')
        request.user.nick_name = nick_name
        request.user.weibo = weibo
        request.user.github = github
        request.user.signature = signature
        request.user.save()
        return HttpResponse('{"status":"0","msg":"修改个人信息成功"}', content_type='application/json')


class UserResetPwdView(LoginRequiredMixin, View):
    """
    登录用户修改密码
    """

    def post(self, request):
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        # 验证用户
        user = authenticate(username=request.user.email, password=password)
        if user is not None:
            request.user.password = make_password(new_password)
            request.user.save()
            logout(request)
            return HttpResponse('{"status":"0","msg":"修改密码成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"1","msg":"修改密码失败"}', content_type='application/json')


class ForgetPwdView(View):
    """
    忘记密码
    """

    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forget.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_email(email, DOMAIN_PREFIX, 'forget')
            return render(request, 'skip.html', {'msg': '重置密码链接已经发送至您的邮箱，请查收！'})
        else:
            return render(request, 'forget.html', {"forget_form": forget_form, 'msg': '输入不合法'})


class ResetPwdView(View):
    """
    重置密码页面
    """

    def get(self, request, code):
        all_recodes = EmailVerifyRecode.objects.filter(code=code)
        if all_recodes:
            for recode in all_recodes:
                email = recode.email
                return render(request, 'resetpwd.html', {'email': email})
        else:
            return render(request, 'skip.html', {'msg': '找回密码失败'})
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    用户未登录修改用户密码
    """

    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            new_password = request.POST.get('new_password', '')
            if password == new_password:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return HttpResponse('{"status":"0","msg":"修改密码成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"1","msg":"两次输入的密码不同"}', content_type='application/json')
        else:
            email = request.POST.get("email", "")
            data = {"status": "2", "msg": email}
            return HttpResponse(json.dumps(data), content_type='application/json')


class UploadImage(LoginRequiredMixin, View):
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
        request.user.image = image_url
        request.user.save()
        return HttpResponseRedirect('/user/setting/')


class UserInfoView(View):
    def get(self, request, user_id):
        # 获取该用户的信息
        user = UserProfile.objects.get(id=user_id)
        # 获取该用户近期创建的话题
        topics = Topic.objects.filter(author=user).order_by('-is_top', '-create_time')[:15]
        # 获取该用户收藏的话题数
        fav_nums = UserFavorite.objects.filter(user=user).count()

        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2))[:10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]

        return render(request, 'userinfo.html', {
            'user': user,
            'topics': topics,
            'fav_nums': fav_nums,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users,
        })


class UserTopicsView(View):
    """
    用户发表的所有话题
    """

    def get(self, request, user_id):
        user = UserProfile.objects.get(id=user_id)
        topics = Topic.objects.filter(author=user).order_by('-is_top', '-create_time')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(topics, 15, request=request)
        page_topics = p.page(page)

        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2)).order_by('-is_top',
                                                                                                             '-create_time')[
                            :10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]
        return render(request, 'usertopics.html', {
            'topics': page_topics,
            'user': user,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users,
        })


class UserFavTopicsView(View):
    """
    用户收藏的话题列表
    """

    def get(self, request, user_id):
        topics = []
        user = UserProfile.objects.get(id=user_id)
        fav_topics = UserFavorite.objects.filter(user=user)
        for fav_topic in fav_topics:
            topic_id = fav_topic.fav_id
            topic = Topic.objects.get(id=topic_id)
            topics.append(topic)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(topics, 15, request=request)
        page_topics = p.page(page)

        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2)).order_by('-is_top',
                                                                                                             '-create_time')[
                            :10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]
        return render(request, 'userfavtopics.html', {
            'user': user,
            'topics': page_topics,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users,
        })


class MessageView(LoginRequiredMixin, View):
    """
    处理我的消息
    """

    def get(self, request):
        # 未读消息
        unread_msgs = UserMessage.objects.filter(to_id=request.user.id, has_read=False).order_by('-send_time')[:15]

        # 过往消息
        readed_msgs = UserMessage.objects.filter(to_id=request.user.id, has_read=True).order_by('-send_time')[:15]

        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]
        return render(request, 'message.html', {
            'user': request.user,
            'unread_msgs': unread_msgs,
            'readed_msgs': readed_msgs,
            'top_users': top_users,
        })


class MessageReadView(LoginRequiredMixin, View):
    def get(self, request, msg_id):
        msg = UserMessage.objects.get(to_id=request.user.id, id=msg_id)
        msg.has_read = True
        msg.save()
        return HttpResponseRedirect(reverse('message'))


class EnrollView(LoginRequiredMixin, View):
    """
    招新
    """

    def get(self, request):
        return render(request, 'enroll.html', {'user': request.user})

    def post(self, request):
        email = request.POST.get('email')
        name = request.POST.get('name')
        class_name = request.POST.get('class_name')
        qq = request.POST.get('qq')
        phone = request.POST.get('phone')
        reason = request.POST.get('reason')

        if UserEnroll.objects.filter(email=email):
            return HttpResponse('{"status":"1","msg":"你已经申请过了"}', content_type='application/json')

        user_enrllo = UserEnroll()
        user_enrllo.email = email
        user_enrllo.name = name
        user_enrllo.class_name = class_name
        user_enrllo.qq = qq
        user_enrllo.phone = phone
        user_enrllo.reason = reason
        user_enrllo.save()
        if user_enrllo.id:
            id = user_enrllo.id
            data = {"status": "0", "msg": "申请成功", "id": id}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('{"status":"1","msg":"申请失败"}', content_type='application/json')


class EnrollDetailView(View):
    def get(self, request, id):
        # 获取该用户的申请信息
        apply_msg = UserEnroll.objects.get(id=id)
        status = "未处理"
        if apply_msg.status == 1:
            status = '未通过'
        elif apply_msg.status == 2:
            status = "已通过"

        apply_user = UserProfile.objects.get(email=apply_msg.email)
        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2)).order_by('-is_top',
                                                                                                             '-create_time')[
                            :10]
        return render(request, 'applydetail.html', {
            'apply_msg': apply_msg,
            'apply_user': apply_user,
            'no_comment_topics': no_comment_topics,
            'status': status,
        })


class EnrollListView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取所有的申请信息
        apply_list = UserEnroll.objects.all()

        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, is_show=True, category__in=(1, 2)).order_by('-is_top',
                                                                                                             '-create_time')[
                            :10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]
        return render(request, 'applylist.html', {
            'user': request.user,
            'apply_list': apply_list,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users,
        })


class UserSetSuperView(LoginRequiredMixin, View):
    """
    设置为超级管理员
    """

    def get(self, request, user_id):
        if request.user.is_superuser:
            user = UserProfile.objects.get(id=user_id)
            user.is_superuser = True
            user.save()

        return HttpResponseRedirect('/user/info/' + user_id)


# 404
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
