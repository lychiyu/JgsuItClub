# -*- coding: utf-8 -*-
__author__ = 'lychiyu'
__date__ = '17-9-17 下午8:55'

import qiniu
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'xxx'
secret_key = 'xxx'

# 构建鉴权对象
q = qiniu.Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'jgsuitclub'
domain_prefix = "http://owcmz09se.bkt.clouddn.com/"


def qiniu_upload_file(file_name, source_file):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, file_name, 3600)
    ret, info = qiniu.put_file(token, file_name, source_file)

    if info.status_code == 200:
        return domain_prefix + ret['key']
    return None
