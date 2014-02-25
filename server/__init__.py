# coding: utf-8

from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_object('config')
    from .api import api, mongo
    api.init_app(app)
    mongo.init_app(app)
    return app

app = create_app()
