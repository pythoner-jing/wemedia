# -*- coding: utf-8 -*-

import os
import logging

DEBUG = True
SECRET_KEY = '\xb2Q"\xce\xb1\xe42b\xcf\xe8\xc1\xcf#]\xb9\xb1\xc5g\x94\x9ba&\xf9&'

# 项目路径
WEMEDIA_PATH = os.path.dirname(__file__)

# 日志
LOG_PATH = os.path.join(os.getcwd(), 'log.txt')
LOG_LEVEL = logging.DEBUG

# 数据库
DB_CONFIG = dict(
    host='localhost',
    user='root',
    passwd='britten',
    db='wemedia',
    charset='utf8',
)

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s?charset=%s' % (
    DB_CONFIG['user'],
    DB_CONFIG['passwd'],
    DB_CONFIG['host'],
    DB_CONFIG['db'],
    DB_CONFIG['charset'],
)

# 分页
PAGE_SIZE = 10
PAGE_GROUP_SIZE = 10

# 编辑器图片上传
UPLOAD_FOLDER = os.path.join(WEMEDIA_PATH, 'uploads')
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

# 最新文章
NEW_ARTICLE_LIMIT = 10

# 文章排行
RANK_ARTICLE_LIMIT = 10

# 邮件配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'zhoujingzhong05@163.com'
MAIL_PASSWORD = 'britten'

DEFAULT_USERNAME = u'匿名用户'
DEFAULT_AVATAR= u'default_avatar.png'
