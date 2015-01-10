# -*- coding: utf-8 -*-

import os
import logging

DEBUG = True

# 项目路径
WEMEDIA_PATH = os.path.dirname(__file__)

# 日志
LOG_PATH = os.path.join(os.getcwd(), 'log.txt')
LOG_LEVEL = logging.DEBUG

# 数据库
DB_CONFIG = dict(
    host='localhost',
    user='root',
    passwd='',
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