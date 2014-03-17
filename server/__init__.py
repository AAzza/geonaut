# coding: utf-8

from flask import Flask
from flask.ext.pymongo import BSONObjectIdConverter

DEFAULT_CONFIG = {
    'DEBUG': True,
    'UPLOAD_TO_DROPBOX': True,
    'MONGO_HOST': '127.0.0.1',
    'MONGO_PORT': 27017,
    'MONGO_DBNAME': 'geonauts',
}

def create_app():
    app = Flask(__name__)
    app.url_map.converters['ObjectId'] = BSONObjectIdConverter

    app.config.update(DEFAULT_CONFIG)
    app.config.from_object('config')
    from .api import api, mongo, dropbox, get_file
    api.init_app(app)
    mongo.init_app(app)

    app.add_url_rule('/files/<path:filename>', 'files', get_file)
    if app.config.get('UPLOAD_TO_DROPBOX'):
        app.config.from_object('dropbox_access_token')
        dropbox.init_app(app)
    return app
