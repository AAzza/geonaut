# encoding: utf-8
import datetime
from StringIO import StringIO

from flask.ext.testing import TestCase
import mongomock
import mock

from server import create_app


pymongo_mock = {
    'init_app.return_value': None,
    'db': mongomock.MongoClient().geonauts,
}

TEST_DROPBOX_URL = 'test.dropbox.test/file'
dropbox_mock = {
    'init_app.return_value': None,
    'client.media.return_value': {'url': TEST_DROPBOX_URL},
    'client.put_file.return_value': {},
}


class BaseTest(TestCase):
    @mock.patch('dropbox.datastore.DatastoreManager')
    @mock.patch('flask.ext.minidrop.Dropbox', return_value=mock.Mock(**dropbox_mock))
    @mock.patch('flask.ext.pymongo.PyMongo', return_value=mock.Mock(**pymongo_mock))
    def create_app(self, mongo, dropbox, datastore_manager):
        app = create_app()
        app.config['TESTING'] = True
        self.db = mongo().db.geonauts
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

    def test_post_unicode(self):
        to_post = {
            'text_content': u'тест',
            'lat': 5,
            'lng': 9,
            'date': datetime.datetime(2013, 11, 10, 0, 0).isoformat()
        }
        resp = self.client.post("/geonotes", data=to_post)
        self.assertStatus(resp, 201)
        self.assertTrue('id' in resp.json)

    def test_post_with_dropbox(self):
        to_post = {
            'text_content': 'test',
            'lat': 5,
            'lng': 9,
            'date': datetime.datetime(2013, 11, 10, 0, 0).isoformat(),
            'media_content': (StringIO('testtesttest'), 'input.txt')
        }
        resp = self.client.post("/geonotes", data=to_post)
        self.assertStatus(resp, 201)
        self.assertTrue('id' in resp.json)
        self.assertTrue('media_content' in resp.json)


class TestGeoNoteApi(BaseTest):
    NOTE1 = {
        'txt': "test",
        'lat': 0,
        'lng': 0,
        'dt': datetime.datetime(2012, 11, 10, 0, 0),
    }

    def test_get(self):
        _id = self.db.insert(self.NOTE1)
        resp = self.client.get('/geonotes/%s' % str(_id))
        self.assert200(resp)
        self.assertEqual(resp.json['id'], str(_id))

    def test_get404(self):
        # bad-formed object_id
        resp = self.client.get('/geonotes/%s' % 100500)
        self.assert400(resp)

        # unexisting, but well-formed object_id
        resp = self.client.get('/geonotes/%s' % '531778be726b5b213f3ece6b')
        self.assert404(resp)

    def test_post_with_dropbox(self):
        to_post = {
            'text_content': 'test',
            'lat': 5,
            'lng': 9,
            'date': datetime.datetime(2013, 11, 10, 0, 0).isoformat(),
            'media_content': (StringIO('testtesttest'), 'input.txt')
        }
        out = self.client.post("/geonotes", data=to_post)
        _id = out.json['id']
        resp = self.client.get('/geonotes/%s' % _id)
        self.assert200(resp)
        self.assertTrue('id' in resp.json)
        self.assertTrue('media_content' in resp.json)
