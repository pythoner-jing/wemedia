# -*- coding: utf-8 -*-

from flask import url_for, render_template, request, redirect, flash, \
    current_app, abort, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy
from flask.ext.login import login_user, logout_user, current_user, login_required
from requests import post, get
from wemedia.common import Common
from models import *
from forms import *

from IPython import embed
from wemedia import db

import json
import time
import wemedia.utils as utils
import hashlib


@Common.route('/')
def index():
    num = Article.query.count()
    lmt = current_app.config['NEW_ARTICLE_LIMIT']
    try:
        new_articles = Article.query.offset(num - lmt).limit(lmt).all()
    except sqlalchemy.exc.ProgrammingError:
        new_articles = []
    return render_template('index.html', new_articles=new_articles)


@Common.route('/article', methods=['GET', 'POST'])
@Common.route('/article/<int:article_id>/', methods=['GET'])
def article(article_id=None):
    form = ArticleForm(request.form)
    if form.validate():
        try:
            filename = utils.save_file(request.files['cover'])
            db.save(Article(form.title.data, form.content.data, form.plain_text.data, filename))
        except AssertionError, err:
            current_app.logger.error(err)
        return redirect('/')
    if article_id:
        a = Article.query.get(article_id)
        return render_template('article.html', article=a)
    return render_template('new-article.html')


@Common.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['upfile']
            filename = utils.save_file(f)
            result = {
                "state": "SUCCESS",
                "url": filename + "/",
                "title": filename,
                "original": filename,
            }
        except AssertionError, err:
            current_app.logger.error(err)
        return json.dumps(result)


@Common.route('/uploads/<filename>/', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)