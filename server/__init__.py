# coding: utf-8

from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError
from flask.ext.pymongo import BSONObjectIdConverter


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.from_object('dropbox_access_token')
    app.url_map.converters['ObjectId'] = BSONObjectIdConverter
    from .api import api, mongo, dropbox
    api.init_app(app)
    mongo.init_app(app)
    dropbox.init_app(app)
    return app
