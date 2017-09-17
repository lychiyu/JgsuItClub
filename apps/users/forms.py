# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 上午10:06'

from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': u'邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': u'密码不能为空', 'invalid': '密码必须大于6位'})
    captcha = CaptchaField(error_messages={'required': u'验证码不能为空', 'invalid': '验证码错误'})


class RegisterForm(forms.Form):
    nick_name = forms.CharField(required=True, error_messages={'required': u'昵称不能为空'})
    email = forms.EmailField(required=True, error_messages={'required': u'邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': u'密码不能为空', 'invalid': '密码必须大于6位'})
    captcha = CaptchaField(error_messages={'required': u'验证码不能为空', 'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': u'邮箱不能为空', 'invalid': '邮箱格式错误'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！'})


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
