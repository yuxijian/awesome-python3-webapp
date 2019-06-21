#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aiohttp import web

__author__ = 'vaeyxj'

' upload handlers '

# from flask import Flask, request
from config import configs
# from coroweb import get, post
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
oss_blog_music_url = 'https://music-info.oss-cn-beijing.aliyuncs.com/'


'''
  文件处理器
'''


class FileHandler(object):
    async def storefile(self, request):
        try:
            reader = await request.multipart()
            file = await reader.next()
            filename = file.filename if file.filename else 'undefined'
            size = 0
            with open('resources/temp/'+filename, 'wb') as f:
                while True:
                    chunk = await file.read_chunk()  # 默认是8192个字节。
                    if not chunk:
                        break
                    size += len(chunk)
                    f.write(chunk)

            # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
            bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
            remote_file_path = "BLOG_MUSIC"+filename
            upload_file = open('resources/temp/'+filename, 'rb')
            result = bucket.put_object(remote_file_path, upload_file, headers={'Content-Type': 'audio/wav'})
            print('[成功上传OSS,file-path:' + oss_blog_music_url + remote_file_path)

            upload_file.close()
            # 删除已经上传的文件
            upload_file_dir = os.getcwd()+'/resources/temp/'
            delList = os.listdir(upload_file_dir)
            for f in delList:
                filePath = os.path.join(upload_file_dir, f)
                if os.path.isfile(filePath):
                    os.remove(filePath)
            return dict(id=1)
        except Exception as e:
            print(e)
            return web.Response(id=0, msg="读取文件数据失败")
