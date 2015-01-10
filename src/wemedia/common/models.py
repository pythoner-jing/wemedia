# -*- coding: utf-8 -*-

import wemedia.utils as utils
import time
import uuid
import json

from wemedia import db


# Article
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    content = db.Column(db.TEXT)
    cover = db.Column(db.String(32))
    plain_text = db.Column(db.TEXT)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, title, content, plain_text, cover):
        self.title = title
        self.content = content
        self.plain_text = plain_text
        self.cover = cover
        self.created = utils.gen_time()
        self.updated = utils.gen_time()

    def __repr__(self):
        return (u'<Article %s>' % self.title).encode('utf-8')


db.drop_all()
db.create_all()