import tornado.testing
import tornado.web
import tornado.escape

from authHandlerDummy import DummyLoginHandler
from volunteerHandler import VolunteerListHandler
from persistence.VolunteerListMongo import PersistentVolunteerList

import logging
import Cookie
import mongomock
import fieldDayTestData

mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)


class TestVolunteerListHandler_unauthenticated(tornado.testing.AsyncHTTPTestCase):

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
        application = tornado.web.Application([(
                    r'/volunteers',
                    VolunteerListHandler,
                    dict(
                        persistentEntityListObj=PersistentVolunteerList(self.mongoCollectionFieldDay)
                    )
                )
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_unauthenticated_list_get(self):
        """ Test that it is not possible to get a Volunteer list without authenticating """
        response = self.fetch("/volunteers", follow_redirects=False)
        self.assertIn(response.code, [302, 403])

    def test_list_unauthenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when un-authenticated is only OPTIONS """

        response = self.fetch(
            "/volunteers",
            method="OPTIONS",
            follow_redirects=False
        )
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))


class TestVolunteerHandler_authenticated(tornado.testing.AsyncHTTPTestCase):

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
                    r'/volunteers',
                    VolunteerListHandler,
                    dict(
                        persistentEntityListObj=PersistentVolunteerList(self.mongoCollectionFieldDay)
                    )
                )
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_authenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when authenticated includes GET """

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )

        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)

        response = self.fetch("/volunteers", method="OPTIONS", follow_redirects=False)
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))


if __name__ == "__main__":
    tornado.testing.main()
