# coding: utf-8

import dateutil.parser

import pymongo
from bson.objectid import ObjectId
import werkzeug
from flask import Flask, make_response, g, request, abort
from flask.ext.restful import Api, reqparse, Resource, fields, marshal

app = Flask(__name__)
api = Api(app)

def get_db():
    if not hasattr(g, 'db'):
        g.db = pymongo.MongoClient('localhost', 27017)['geonotes'].notes
    return g.db

str2date = lambda s: dateutil.parser.parse(s)

parser = reqparse.RequestParser()
parser.add_argument('lat', type=int, required=True, help='Latitude of the note')
parser.add_argument('lng', type=int, required=True, help='Longitude of the note')
parser.add_argument('date', type=str2date, required=True, help='Date, when note was created')
parser.add_argument('text_content', type=str, help='Note content')
# parser.add_argument('media_content', type=werkzeug.datastructures.FileStorage,
#                     location='files', help='Note media content')


note_fields = {
    'id': fields.String(attribute="_id"),
    'lat': fields.Integer,
    'lng': fields.Integer,
    'date': fields.DateTime(attribute='dt'),
    'text_content': fields.String(attribute='txt'),
    # 'media_content': fields.String,
}


class Notes(Resource):
    def get(self):
        return [marshal(note, note_fields) for note in get_db().find()]

    def post(self):
        args = parser.parse_args()
        new_note = {
            'lat': args.lat,
            'lng': args.lng,
            'dt': args.date,
            'txt': args.text_content,
        }
        new_note['id_'] = get_db().insert(new_note)
        return marshal(new_note, note_fields), 201


class Note(Resource):
    def get(self, note_id):
        note = get_db().find_one(ObjectId(note_id))
        if not note:
            abort(404)
        return marshal(note, note_fields)


api.add_resource(Notes, '/geonotes')
api.add_resource(Note, '/geonotes/<string:note_id>')


@app.route('/')
def index():
    return make_response(open('static/index.html').read())
