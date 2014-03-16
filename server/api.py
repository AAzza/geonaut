# encoding: utf-8

import os
from datetime import datetime

import dateutil.parser

import werkzeug
from flask import abort, current_app
from flask.ext.restful import Api, reqparse, Resource, fields, marshal
from flask.ext.pymongo import PyMongo
from flask.ext.minidrop import Dropbox
from dropbox.datastore import Date, DatastoreManager


api = Api()
mongo = PyMongo()
dropbox = Dropbox()


str2date = lambda s: dateutil.parser.parse(s)

def datetime2timestamp(dt, epoch=datetime(1970,1,1)):
    dt = dt.replace(tzinfo=None)
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6


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
        if args.media_content and current_app.config["UPLOAD_TO_DROPBOX"]:
            _, ext = os.path.splitext(args.media_content.filename)
            filename = '/%s%s' % (new_note['_id'], ext)
            metadata = dropbox.client.put_file(filename, args.media_content)
            media_url = dropbox.client.media(filename)['url']
            mongo.db.geonauts.update({'_id': new_note['_id']}, {'$set': {'url': media_url}})
            new_note['url'] = media_url

        #backup also info to dropbox-datastore
        if current_app.config["UPLOAD_TO_DROPBOX"]:
            datastore = DatastoreManager(dropbox.client).open_default_datastore()
            notes_table = datastore.get_table('geonotes')
            def do_insert():
                drop_note = {
                    '_id': str(new_note['_id']),
                    'lat': new_note['lat'],
                    'lng': new_note['lng'],
                    'date': Date(datetime2timestamp(new_note['dt'])),
                    'text_content': new_note['txt'],
                }
                if 'url' in new_note:
                    drop_note['media_content'] = new_note['url']
                notes_table.insert(**drop_note)
            datastore.transaction(do_insert, max_tries=4)
        return marshal(new_note, note_fields), 201


class Note(Resource):
    def get(self, note_id):
        note = mongo.db.geonauts.find_one(note_id)
        if not note:
            abort(404)
        return marshal(note, note_fields)


api.add_resource(Notes, '/geonotes')
api.add_resource(Note, '/geonotes/<ObjectId:note_id>')
