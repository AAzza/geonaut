# encoding: utf-8

import os
from base64 import urlsafe_b64encode

import dateutil.parser

import werkzeug
from flask import abort
from flask.ext.restful import Api, reqparse, Resource, fields, marshal
from flask.ext.pymongo import PyMongo
from flask.ext.minidrop import Dropbox


api = Api()
mongo = PyMongo()
dropbox = Dropbox()


str2date = lambda s: dateutil.parser.parse(s)

parser = reqparse.RequestParser()
parser.add_argument('lat', type=float, required=True, help='Latitude of the note')
parser.add_argument('lng', type=float, required=True, help='Longitude of the note')
parser.add_argument('date', type=str2date, required=True, help='Date, when note was created')
parser.add_argument('text_content', type=str, help='Note content')
parser.add_argument('media_content', type=werkzeug.datastructures.FileStorage,
                    location='files', help='Note media content')


class ObjectIdField(fields.Raw):
    def format(self, value):
        return str(value)


note_fields = {
    'id': ObjectIdField(attribute="_id"),
    'lat': fields.Float,
    'lng': fields.Float,
    'date': fields.DateTime(attribute='dt'),
    'text_content': fields.String(attribute='txt'),
    'media_content': fields.String(attribute='url'),
}


class Notes(Resource):
    def get(self):
        return [marshal(note, note_fields) for note in mongo.db.geonauts.find()]

    def post(self):
        args = parser.parse_args()
        new_note = {
            'lat': args.lat,
            'lng': args.lng,
            'dt': args.date,
            'txt': args.text_content,
        }
        new_note['_id'] = mongo.db.geonauts.insert(new_note)
        #add to dropbox
        if args.media_content:
            _, ext = os.path.splitext(args.media_content.filename)
            filename = '/%s%s' % (new_note['_id'], ext)
            metadata = dropbox.client.put_file(filename, args.media_content)
            media_url = dropbox.client.media(filename)['url']
            mongo.db.geonauts.update({'_id': new_note['_id']}, {'$set': {'url': media_url}})
            new_note['url'] = media_url
        return marshal(new_note, note_fields), 201


class Note(Resource):
    def get(self, note_id):
        note = mongo.db.geonauts.find_one(note_id)
        if not note:
            abort(404)
        return marshal(note, note_fields)


api.add_resource(Notes, '/geonotes')
api.add_resource(Note, '/geonotes/<ObjectId:note_id>')
