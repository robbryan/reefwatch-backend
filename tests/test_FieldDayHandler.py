import tornado.testing
import tornado.web
import tornado.escape

from authHandlerDummy import DummyLoginHandler
from baseHandler import BaseHandler
from fieldDayHandler import FieldDayHandler
from persistence.FieldDayMongo import PersistentFieldDay

import logging
import Cookie
import mongomock
import fieldDayTestData


class TestFieldDayTidesHandler_unauthenticated(tornado.testing.AsyncHTTPTestCase):

    __cookieSecret__ = "THIS_IS_THE_TEST_COOKIE_SECRET"

    def __init__(self, *rest):
        self.cookies = Cookie.SimpleCookie()
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    @classmethod
    def setUpClass(cls):
        cls.mongoCollectionFieldDay = mongomock.MongoClient().db.collection
        for obj in fieldDayTestData.fieldDayList:
            cls.mongoCollectionFieldDay.insert(obj)

    @classmethod
    def tearDownClass(cls):
        pass

    def get_app(self):
        application = tornado.web.Application([
                (
                    r'/field_days/([A-Za-z0-9]+)',
                    FieldDayHandler,
                    dict(persistentEntityObj=PersistentFieldDay(self.mongoCollectionFieldDay))
                )
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_unauthenticatedGET(self):
        """ Test that it's possible to get Field Day Tides without authenticating """

        """ Find a Field Day with a Tides collection with at least one tide """
        for fieldDayId in [x["_id"] for x in fieldDayTestData.fieldDayList]:

            response = self.fetch("/field_days/{field_day_id}".format(field_day_id=fieldDayId), follow_redirects=False)
            self.assertEqual(response.code, 200)
            responseJson = tornado.escape.json_decode(response.body)
            self.assertTrue(any(responseJson))

    def test_unauthenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when un-authenticated is only GET """

        """ Find a Field Day with a Tides collection with at least one tide """
        fieldDayId = filter(lambda x: 'tides' in x and any(x['tides']), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch("/field_days/{field_day_id}".format(field_day_id=fieldDayId), method="OPTIONS", follow_redirects=False)
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_unauthenticatedPUTT(self):
        """ Test that PUT is not allowed when un-authenticated """

        """ Find a Field Day """
        fieldDayId = filter(lambda x: any(x), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch(
            "/field_days/{field_day_id}".format(
                field_day_id=fieldDayId
            ),
            method="PUT",
            body=tornado.escape.json_encode({}),
            follow_redirects=False
        )
        self.assertIn(response.code, [302, 403])


class TestFieldDayHandler_authenticated(tornado.testing.AsyncHTTPTestCase):

    __cookieSecret__ = "THIS_IS_THE_TEST_COOKIE_SECRET"

    def __init__(self, *rest):
        self.cookies = Cookie.SimpleCookie()
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    @classmethod
    def setUpClass(cls):
        cls.mongoCollectionFieldDay = mongomock.MongoClient().db.collection
        for obj in fieldDayTestData.fieldDayList:
            cls.mongoCollectionFieldDay.insert(obj)

    @classmethod
    def tearDownClass(cls):
        pass

    def _update_cookies(self, headers):
        try:
            sc = headers['Set-Cookie']
            cookies = tornado.escape.native_str(sc)
            self.cookies.update(Cookie.SimpleCookie(cookies))
            while True:
                self.cookies.update(Cookie.SimpleCookie(cookies))
                if ',' not in cookies:
                    break
                cookies = cookies[cookies.find(',') + 1:]
        except KeyError:
            return
        print self.cookies

    def fetch(self, url, *r, **kw):
        if 'follow_redirects' not in kw:
            kw['follow_redirects'] = False
        header = {}
        hs = self.cookies.output()
        if hs != '':
            if ";" in hs:
                hs = ":".join(hs.split(":")[1:]).split(";")[0].strip()
            else:
                hs = hs.split(':')[1]
            header['Cookie'] = hs
            #print "URL: {}, Cookie: {}".format(url, header['Cookie'])
        resp = tornado.testing.AsyncHTTPTestCase.fetch(self, url, headers=header, *r, **kw)
        self._update_cookies(resp.headers)
        return resp

    def get_app(self):
        application = tornado.web.Application([
                (
                    r"/auth/login/dummy",
                    DummyLoginHandler,
                    dict(persistentUserListObj=None)
                ),
                (
                    r'/field_days/([A-Za-z0-9]+)',
                    FieldDayHandler,
                    dict(persistentEntityObj=PersistentFieldDay(self.mongoCollectionFieldDay))
                )
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_authenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when authenticated includes PUT """

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )

        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)

        """ Find a Field Day """
        fieldDayId = filter(lambda x: any(x), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch("/field_days/{field_day_id}".format(field_day_id=fieldDayId), method="OPTIONS", follow_redirects=False)
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS", "PUT"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_nonexistent_field_day_update(self):
        """ Negative test - Updating a Field Day which does not exist """

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )

        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)

        """ Find a Field Day with no Site attribute """
        fieldDayId = "000000000000000000000000"
        tides = tornado.escape.json_encode(
            {
                "high": {"time": "05:17:00", "height": 0.77}
            }
        )
        response = self.fetch(
            "/field_days/{field_day_id}/tides".format(
                field_day_id=fieldDayId
            ),
            method="POST",
            body="tides={tides}".format(tides=tides),
            follow_redirects=False
        )
        self.assertEqual(response.code, 404)

if __name__ == "__main__":
    tornado.testing.main()
