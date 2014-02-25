# encoding: utf-8
import datetime
from base64 import urlsafe_b64encode

from flask.ext.testing import TestCase
import mongomock
import mock

from server import create_app


class MockPyMongo(object):
    db = mongomock.MongoClient().geonauts

    def init_app(self, app):
        pass


class BaseTest(TestCase):
    @mock.patch('flask.ext.pymongo.PyMongo', new_callable=lambda: MockPyMongo)
    def create_app(self, mongo):
        app = create_app()
        app.config['TESTING'] = True
        self.db = mongo.db.geonauts
        return app

    def setUp(self):
        self.db.remove()


class TestGeoNotesApi(BaseTest):
    NOTE1 = {
        'txt': "test",
        'lat': 0,
        'lng': 0,
        'dt': datetime.datetime(2012, 11, 10, 0, 0),
    }

    NOTE2 = {
        'txt': "test",
        'lat': 0,
        'lng': 0,
        'dt': datetime.datetime(2012, 11, 10, 0, 0),
    }

    def test_get_empty(self):
        resp = self.client.get("/geonotes")
        self.assert200(resp)
        self.assertEquals(resp.json, [])

    def test_get(self):
        _id = self.db.insert(self.NOTE1)
        resp = self.client.get("/geonotes")
        self.assert200(resp)
        self.assertEquals(len(resp.json), 1)

    def test_get_several(self):
        _id1 = self.db.insert(self.NOTE1)
        _id2 = self.db.insert(self.NOTE2)
        resp = self.client.get("/geonotes")
        self.assert200(resp)
        self.assertEquals(len(resp.json), 2)

    def test_post_one_error(self):
        resp = self.client.post("/geonotes", {})
        self.assert400(resp)

        resp = self.client.post("/geonotes", {'lat': 9})
        self.assert400(resp)

    def test_post_one(self):
        to_post = {
            'text_content': 'test',
            'lat': 5,
            'lng': 9,
            'date': datetime.datetime(2013, 11, 10, 0, 0).isoformat()
        }
        resp = self.client.post("/geonotes", data=to_post)
        self.assertStatus(resp, 201)
        self.assertTrue('id' in resp.json)


class TestGeoNoteApi(BaseTest):
    NOTE1 = {
        'txt': "test",
        'lat': 0,
        'lng': 0,
        'dt': datetime.datetime(2012, 11, 10, 0, 0),
    }

    def test_get(self):
        _id = self.db.insert(self.NOTE1)
        hash_id = urlsafe_b64encode(_id.binary)
        resp = self.client.get('/geonotes/%s' % hash_id)
        self.assert200(resp)
        self.assertEqual(resp.json['id'], str(hash_id))

    def test_get404(self):
        # bad-formed object_id
        resp = self.client.get('/geonotes/%s' % 100500)
        self.assert404(resp)

        # unexisting, but well-formed object_id
        resp = self.client.get('/geonotes/%s' % 'UwzFp3JrW3BCFp7v')
        self.assert404(resp)
