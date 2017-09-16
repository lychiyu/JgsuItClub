# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-16 上午10:53'

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecode
from JgsuItClub.settings import EMAIL_FROM

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_email(email, host, send_type='register'):
    email_code = EmailVerifyRecode()
    if send_type == 'update_email':
        code = random_str(6)
    else:
        code = random_str(16)

    email_code.code = code
    email_code.email = email
    email_code.send_type = send_type
    email_code.save()

    # 注册激活
    if send_type == 'register':
        email_title = '注册技术交流社区网激活链接'
        email_body = '请复制下面的链接在浏览器中打开以激活你的账号： {0}/active/{1}'.format(host, code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    # 忘记密码激活
    if send_type == 'forget':
        email_title = '技术交流社区网密码重置链接'
        email_body = '请复制下面的链接在浏览器中打开以重置你的密码： {0}/reset/{1}'.format(host, code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
