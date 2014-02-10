# coding: utf-8

import datetime

import werkzeug
from flask import Flask
from flask.ext.restful import Api, reqparse, Resource, fields, marshal


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('lat', type=int, required=True, help='Latitude of the note')
parser.add_argument('lng', type=int, required=True, help='Latitude of the note')
parser.add_argument('date', type=datetime, required=True, help='Date, when note was created')
parser.add_argument('text_content', type=str, help='Note content')
parser.add_argument('media_content', type=werkzeug.datastructures.FileStorage,
                    location='files', help='Note media content')

db = [{
    'lat': 0,
    'lng': 1,
    'date': datetime.datetime.now(),
    'text_content': 'Some text here',
}]

note_fields = {
    'lat': fields.Integer,
    'lng': fields.Integer,
    'date': fields.DateTime,
    'text_content': fields.String,
    'media_content': fields.String,
}


class GeoNotes(Resource):
    def get(self):
        return {'notes': [marshal(note, note_fields) for note in db]}

    def post(self):
        args = parser.parse_args()
        db.extend(args)
        return 'ok', 201


api.add_resource(GeoNotes, '/geonotes')
