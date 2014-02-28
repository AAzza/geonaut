# coding: utf-8

from base64 import urlsafe_b64encode, urlsafe_b64decode

from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError
from bson.objectid import ObjectId
from bson.errors import InvalidId


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(urlsafe_b64decode(str(value)))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return urlsafe_b64encode(value.binary)


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_object('config')
    app.config.from_object('dropbox_access_token')
    app.url_map.converters['objectid'] = ObjectIDConverter
    from .api import api, mongo, dropbox
    api.init_app(app)
    mongo.init_app(app)
    dropbox.init_app(app)
    return app
