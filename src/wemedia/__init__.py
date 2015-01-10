# -*- coding: utf-8 -*-

import wemedia.settings
import logging
import logging.handlers
import wemedia.utils as utils
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = None


class DB(SQLAlchemy):
    def __init__(self, app):
        SQLAlchemy.__init__(self, app)

    def update(self, data):
        data.updated = utils.gen_time()
        self.session.commit()

    def save(self, data):
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, data):
        data.deleted = True
        self.update(data)

    def real_delete(self, data):
        self.session.delete(data)
        self.session.commit()


def create_app():
    global db

    app = Flask(__name__)

    app.config.from_object(wemedia.settings)

    db = DB(app)

    setup_blueprints(app)
    setup_logger(app)

    return app


def setup_blueprints(app):
    from wemedia.common import Common

    app.register_blueprint(Common, url_prefix='')


def setup_logger(app):
    log_path = wemedia.settings.LOG_PATH
    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='d',
                                                        interval=1)
    handler.setLevel(wemedia.settings.LOG_LEVEL)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)