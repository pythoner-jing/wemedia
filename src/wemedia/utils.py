#!/usr/bin/env python
# -*- coding: utf-8 -*-


import settings
import cStringIO
import time
import hashlib
import os

from functools import wraps
from flask import send_file, current_app
from requests import get
from werkzeug import secure_filename
from threading import Thread
from flask.ext.mail import Mail, Message


# 异步装饰器
def async(f):
    def wrapper(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)
        t.start()
    return wrapper


# 分页
def paging(page_num, model_query, page_size=settings.PAGE_SIZE,
           page_group_size=settings.PAGE_GROUP_SIZE):
    last = model_query.count() / page_size if model_query.count() % page_size == 0 else \
        model_query.count() / page_size + 1
    assert 1 <= page_num <= last, u'page_num must be in [1, last]'
    offset = (page_num - 1) * page_size
    entities = model_query.offset(offset).limit(page_size).all()
    if last < page_group_size:
        page_group_size = last
    start = page_num - page_group_size / 2 - page_group_size % 2
    start = start if start > 0 else 0
    if last - start < page_group_size:
        start = last - page_group_size

    return dict(
        last=last,
        current=page_num,
        page_group=range(start + 1, start + 1 + page_group_size),
        entities=entities,
    )


# 图片缩放
# def zoom(uri, size):
#     f = cStringIO.StringIO(get(uri, proxies=settings.PROXIES).content)
#     img = Image.open(f)
#     target_img = img.resize(size, Image.ANTIALIAS)
#     img_io = cStringIO.StringIO()
#     target_img.save(img_io, 'JPEG')
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/jpeg')


# 判断上传图片合法性
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


# 返回当前时间
def gen_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


# 保存文件
def save_file(f):
    assert f and allowed_file(f.filename), u'file is not exist or diallowed'
    filename = secure_filename(f.filename)
    enc = hashlib.md5()
    enc.update(filename)
    enc.update(str(time.time()))
    filename = enc.hexdigest()
    f.save(os.path.join(settings.UPLOAD_FOLDER, filename))
    return filename


# 发送邮件
def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail = Mail(current_app)
    mail.send(msg)
