# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from users.models import UserProfile
from users.forms import RegisterForm, LoginForm
from utils.email_send import send_email
from topics.models import Topic, Category


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
        host = request.get_host()
        scheme = str(request.scheme)
        hosts = scheme + '://' + str(host)
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
            send_email(email, hosts)
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


class IndexView(View):
    def get(self, request):
        # 获取所有话题分类
        cates = Category.objects.all()
        # 获取所有话题
        topics = Topic.objects.all()

        # 无人回复的话题
        no_comment_topics = Topic.objects.filter(comment_nums=0, category__in=(1, 2))[:10]
        # 积分榜
        top_users = UserProfile.objects.all().order_by('-score')[:15]
        return render(request, 'index.html', {
            'cates': cates,
            'topics': topics,
            'no_comment_topics': no_comment_topics,
            'top_users': top_users
        })
