import datetime

from flask.ext.testing import TestCase
import mongomock
import mock

from server import app, get_db

class BaseTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.mongo_patcher = mock.patch('pymongo.MongoClient', mongomock.MongoClient)
        self.mongo_patcher.start()

    def tearDown(self):
        self.mongo_patcher.stop()


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
        _id = get_db().insert(self.NOTE1)
        resp = self.client.get("/geonotes")
        self.assert200(resp)
        self.assertEquals(len(resp.json), 1)
        self.assertEqual(resp.json[0]['id'], str(_id))

    def test_get_several(self):
        _id1 = get_db().insert(self.NOTE1)
        _id2 = get_db().insert(self.NOTE2)
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
        id_ = get_db().insert(self.NOTE1)
        resp = self.client.get('/geonotes/%s' % id_)
        self.assert200(resp)
        self.assertEqual(resp.json['id'], str(id_))


