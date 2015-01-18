# -*- coding: utf-8 -*-

from wtforms import Form, PasswordField, validators, StringField, DateField, FileField


class ArticleForm(Form):
    title = StringField('title', [validators.DataRequired(), validators.Length(max=200)])
    content = StringField('content', [validators.DataRequired()])
    plain_text = StringField('plain_text', [validators.DataRequired()])


class ArticleUpdateForm(Form):
    title = StringField('title', [validators.DataRequired(), validators.Length(max=200)])
    content = StringField('content', [validators.DataRequired()])
    plain_text = StringField('plain_text', [validators.DataRequired()])


class LoginForm(Form):
    email = StringField('email', [validators.DataRequired(), validators.Length(max=320)])
    password = PasswordField('password', [validators.DataRequired()])


class RegistryForm(Form):
    email = StringField('email', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
