# -*- coding: utf-8 -*-

import wemedia.utils as utils

from wemedia import db
from flask.ext.login import UserMixin
from wemedia import settings
from flask import url_for

import hashlib
import time
import random


# 文章
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    content = db.Column(db.TEXT)
    plain_text = db.Column(db.TEXT)
    clicks = db.Column(db.Integer, default=0)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)
    deleted = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, author, title, content, plain_text):
        self.author = author
        self.title = title
        self.content = content
        self.plain_text = plain_text
        self.created = utils.gen_time()
        self.updated = utils.gen_time()

    def __repr__(self):
        return (u'<Article %s>' % self.title).encode('utf-8')


# 用户
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    activated = db.Column(db.Boolean, default=False)
    activate_code = db.Column(db.String(32))
    username = db.Column(db.String(50))
    password = db.Column(db.String(32))
    avatar = db.Column(db.String(32))
    email = db.Column(db.String(320))

    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, username=settings.DEFAULT_USERNAME, avatar=settings.DEFAULT_AVATAR):
        self.email = email
        self.username = username
        self.password = password
        self.avatar = avatar
        enc = hashlib.md5()
        enc.update(email)
        enc.update(str(random.random()))
        self.activate_code = enc.hexdigest()


    def __repr__(self):
        return (u'<User %s>' % self.username).encode('utf-8')


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))

    content = db.Column(db.TEXT)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article', backref=db.backref('comments', lazy='dynamic'))

    quote_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    quote = db.relationship('Comment', backref=db.backref('comments'), remote_side=[id])

    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, article_id, author, content, quote_id):
        self.article_id = article_id
        self.author = author
        self.content = content
        self.quote_id = quote_id


# db.drop_all()
db.create_all()
