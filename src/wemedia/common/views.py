# -*- coding: utf-8 -*-

from flask import url_for, render_template, request, redirect, flash, \
    current_app, abort, send_from_directory, copy_current_request_context
from flask.ext.login import login_user, logout_user, current_user, login_required
from wemedia.common import Common
from models import User, Article, Comment
from forms import ArticleForm, LoginForm, ArticleUpdateForm, RegistryForm, \
        CommentForm
from IPython import embed
from wemedia import db
from threading import Thread
from wemedia import utils as utils

import json
import hashlib


@Common.route('/')
def index():
    article_count = Article.query.count()
    new_lmt = current_app.config['NEW_ARTICLE_LIMIT']
    rank_lmt = current_app.config['RANK_ARTICLE_LIMIT']

    new_offset = article_count - new_lmt if article_count > new_lmt else 0
    rank_offset = article_count - rank_lmt if article_count > rank_lmt else 0

    new_articles = Article.query.filter_by(deleted=False).offset(new_offset).limit(new_lmt).all()
    rank_articles = Article.query.filter_by(deleted=False).order_by(Article.clicks.desc()).offset(rank_offset).limit(rank_lmt).all()

    return render_template('index.html', new_articles=new_articles, rank_articles=rank_articles)


@Common.route('/article/<int:article_id>/', methods=['GET'])
def article(article_id):
    a = Article.query.get(article_id)
    a.clicks += 1
    db.update(a)

    return render_template('article.html', article=a)



@Common.route('/article/new/', methods=['GET', 'POST'])
@login_required
def article_new():
    form = ArticleForm(request.form)
    if form.validate():
        try:
            db.save(Article(current_user, form.title.data, form.content.data, form.plain_text.data))
        except AssertionError, err:
            current_app.logger.error(err)
        return redirect(url_for('Common.index'))

    return render_template('new-article.html')

@Common.route('/article/delete/<int:article_id>/', methods=['GET'])
@login_required
def article_delete(article_id):
    a = Article.query.get(article_id)
    assert current_user == a.author, abort(401)
    db.delete(a)
    return redirect(url_for('Common.index'))


@Common.route('/article/update/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def article_update(article_id):
    form = ArticleUpdateForm(request.form)
    if form.validate():
        a = Article.query.get(article_id)
        assert a.author == current_user, abort(401)
        a.title = form.title.data
        a.content = form.content.data
        a.plain_text = form.plain_text.data
        db.update(a)
        return redirect(url_for('Common.index'))

    a = Article.query.get(article_id)
    return render_template('update-article.html', article=a)


@Common.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data
        password = hashlib.md5(form.password.data).hexdigest()
        u = User.query.filter_by(email=email, password=password, activated=not current_app.config['DEBUG']).first()
        if u:
            login_user(u)
            return redirect(url_for('Common.index'))
        else:
            flash(u'用户名或密码有误', u'error')

    return render_template('login.html')


@Common.route('/registry', methods=['GET', 'POST'])
def registry():
    form = RegistryForm(request.form)

    if form.validate():
        email = form.email.data
        u = User.query.filter_by(email=email).first()
        if u:
            flash(u'邮箱已被注册', u'error')
        else:
            new_user = User(form.email.data, hashlib.md5(form.password.data).hexdigest())
            db.save(new_user)
            text_body = html_body = render_template('activate.html', user_id=new_user.id, activate_code=new_user.activate_code)
            @copy_current_request_context
            def send_async_email():
                utils.send_mail(u'自媒体帐号激活', current_app.config['MAIL_USERNAME'], [form.email.data], text_body, html_body)
            Thread(target=send_async_email).start()
            if current_app.config['DEBUG']:
                login_user(new_user)
            flash(u'已向你的邮箱 %s 发送激活邮件,请确认并激活你的自媒体帐号' % form.email.data, u'info')
            return render_template('message.html')

    return render_template('registry.html')


@Common.route('/logout', methods=['GET'])
def logout():
    logout_user()

    return redirect(url_for('Common.login'))


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


@Common.route('/activate/<int:user_id>/<activate_code>/', methods=['GET'])
def activate(user_id, activate_code):
    u = User.query.filter_by(id=user_id, activate_code=activate_code).first()
    if u:
        flash(u'激活帐号成功', u'success')
        login_user(u)
    else:
        flash(u'激活帐号失败', u'danger')

    return render_template('message.html')


@Common.route('/comment/new/', methods=['POST'])
@login_required
def comment_new():
    form = CommentForm(request.form)

    if form.validate():
        form.quote_id.data = None if form.quote_id.data < 0 else form.quote_id.data
        c = Comment(form.article_id.data, current_user, form.content.data, form.quote_id.data)
        db.save(c)

        return redirect(url_for('Common.article', article_id=form.article_id.data))

    return redirect(url_for('Common.index'))


@Common.route('/comment/delete/<int:article_id>/<int:comment_id>/', methods=['GET'])
def comment_delete(article_id, comment_id):
   c = Comment.query.get(comment_id)
   db.delete(c)

   return redirect(url_for('Common.article', article_id=article_id))
