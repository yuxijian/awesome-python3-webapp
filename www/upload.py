#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'vaeyxj'

' upload handlers '

# from flask import Flask, request
from config import configs
from coroweb import get, post
from werkzeug.utils import secure_filename
import os
import oss2
# from werkzeug.test import EnvironBuilder

# app = Flask(__name__)
# ctx = app.request_context(EnvironBuilder('/', 'http://localhost/').get_environ())
# ctx.push()
# ctx = app.app_context()
# ctx.push()


COOKIE_NAME = 'VAE-YXJ-SESSION'
_COOKIE_KEY = configs.session.secret

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIBIeK1jN1C6Nk')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'yuy7mNgw0I3oDDwBlN11riffUiTvg2')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'music-info')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')


@post('/api/upload/music')
def api_upload_music(request):
    # 确认上面的参数都填写正确了
    for param in (access_key_id, access_key_secret, bucket_name, endpoint):
        assert '<' not in param, '请设置参数：' + param

    upload_file = request.files['file-0']
    filename = secure_filename(upload_file.filename)

    # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    remote_file_path = "BLOG_MUSIC_DIR"
    # streamReader = request.content
    # result = bucket.put_object_from_file(remote_file_path, streamReader)
    return dict(id=1)

