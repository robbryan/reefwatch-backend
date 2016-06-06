import tornado.testing
import tornado.web
import tornado.escape

from authHandlerDummy import DummyLoginHandler
from fieldDaySiteHandler import FieldDaySiteListHandler, FieldDaySiteHandler
from persistence.FieldDaySiteListMongo import PersistentFieldDaySiteList
from persistence.FieldDaySiteMongo import PersistentFieldDaySite

from persistence.LocationMongo import PersistentLocation

import logging
import Cookie
import mongomock
import fieldDayTestData

mongoCollectionLocation = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.locationList:
    mongoCollectionLocation.insert(obj)

from persistence.FieldDayMongo import PersistentFieldDay


class TestFieldDaySitesHandler_unauthenticated(tornado.testing.AsyncHTTPTestCase):

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
                    r'/field_days/([A-Za-z0-9]+)/sites/([A-Za-z]{2,})',
                    FieldDaySiteHandler,
                    dict(
                        persistentFieldDaySiteEntityObj=PersistentFieldDaySite(self.mongoCollectionFieldDay)
                    )
                ),
                (
                    r'/field_days/([A-Za-z0-9]+)/sites',
                    FieldDaySiteListHandler,
                    dict(
                        persistentFieldDaySiteListObj=PersistentFieldDaySiteList(self.mongoCollectionFieldDay),
                        persistentLocationEntityObj=PersistentLocation(mongoCollectionLocation),
                        persistentFieldDayEntityObj=PersistentFieldDay(self.mongoCollectionFieldDay)
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
        """ Test that it's possible to get Field Day Sites without authenticating """

        """ Find a Field Day with a Sites collection with at least one site """
        for fieldDay in filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList):
            fieldDayId = fieldDay["_id"]
            print "Field Day ID: {}".format(fieldDayId)
            response = self.fetch("/field_days/{field_day_id}/sites".format(field_day_id=fieldDayId), follow_redirects=False)
            self.assertEqual(response.code, 200)
            responseJson = tornado.escape.json_decode(response.body)
            self.assertTrue(any(responseJson))

    def test_unauthenticated_site_get(self):
        """ Test that it's possible to get Field Day Sites without authenticating """

        """ Find a Field Day with a Sites collection with at least one site """
        fieldDay = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList)[0]
        fieldDayId = fieldDay["_id"]
        for fieldDaySite in fieldDay["sites"]:
            siteCode = fieldDaySite["site_code"] 
            print "Field Day ID: {}".format(fieldDayId)
            response = self.fetch(
                "/field_days/{field_day_id}/sites/{site_code}".format(
                    field_day_id=fieldDayId,
                    site_code=siteCode
                ),
                follow_redirects=False
            )
            self.assertEqual(response.code, 200)
            responseJson = tornado.escape.json_decode(response.body)
            self.assertTrue(any(responseJson))

    def test_negative_field_day_does_not_exist(self):
        """ Test requesting a Field Day Site that doesn't exist results in a 404 """

        """ Find a Field Day with a Sites collection with at least one site """
        fieldDayId = "000000000000000000000000"
        response = self.fetch("/field_days/{field_day_id}/sites".format(field_day_id=fieldDayId), follow_redirects=False)
        self.assertEqual(response.code, 404)

    def test_negative_site_does_not_exist(self):
        """ Test requesting a Field Day Site that doesn't exist results in a 404 """

        """ Find a Field Day with a Sites collection with at least one site """
        fieldDay = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList)[0]
        fieldDayId = fieldDay["_id"]
        siteCode = "XXX" # I hope that this one doesn't exist
        response = self.fetch("/field_days/{field_day_id}/sites/{site_code}".format(field_day_id=fieldDayId, site_code = siteCode), follow_redirects=False)
        self.assertEqual(response.code, 404)

    def test_list_unauthenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when un-authenticated is only GET """

        """ Find a Field Day with a Sites collection with at least one site """
        fieldDayId = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch(
            "/field_days/{field_day_id}/sites".format(field_day_id=fieldDayId),
            method="OPTIONS",
            follow_redirects=False
        )
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_site_unauthenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when un-authenticated is only GET """

        """ Find a Field Day with a Sites collection with at least one site """
        fieldDay = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList)[0]
        fieldDayId = fieldDay["_id"]
        siteCode = fieldDay["sites"][0]["site_code"]
        response = self.fetch(
            "/field_days/{field_day_id}/sites/{site_code}".format(
                field_day_id=fieldDayId,
                site_code=siteCode
            ),
            method="OPTIONS",
            follow_redirects=False
        )
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_list_unauthenticatedPOST(self):
        """ Test that POST is not allowed when un-authenticated """

        """ Find a Field Day """
        fieldDayId = filter(lambda x: any(x), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch(
            "/field_days/{field_day_id}/sites".format(
                field_day_id=fieldDayId
            ),
            method="POST",
            body=tornado.escape.json_encode({}),
            follow_redirects=False
        )
        self.assertIn(response.code, [403])

    def test_site_unauthenticatedPOST(self):
        """ Test that POST is not allowed when un-authenticated """

        """ Find a Field Day """
        fieldDay = filter(lambda x: any(x), fieldDayTestData.fieldDayList)[0]
        fieldDayId = fieldDay["_id"]
        siteCode = fieldDay["sites"][0]["site_code"]
        response = self.fetch(
            "/field_days/{field_day_id}/sites/{site_code}".format(
                field_day_id=fieldDayId,
                site_code=siteCode
            ),
            method="POST",
            body=tornado.escape.json_encode({}),
            follow_redirects=False
        )
        self.assertIn(response.code, [405])


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
                    DummyLoginHandler
                ),
                (
                    r'/field_days/([A-Za-z0-9]+)/sites',
                    FieldDaySiteListHandler,
                    dict(
                        persistentFieldDaySiteListObj=PersistentFieldDaySiteList(self.mongoCollectionFieldDay),
                        persistentLocationEntityObj=PersistentLocation(mongoCollectionLocation),
                        persistentFieldDayEntityObj=PersistentFieldDay(self.mongoCollectionFieldDay)
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
        """ Test that OPTIONS allowed when authenticated includes POST """

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )

        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)

        """ Find a Field Day with a Sites collection """
        fieldDayId = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.fieldDayList)[0]["_id"]
        response = self.fetch("/field_days/{field_day_id}/sites".format(field_day_id=fieldDayId), method="OPTIONS", follow_redirects=False)
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS", "POST"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_site_post_to_nonexistent(self):
        """ add a site to a Field Day that does not have a Sites collection """

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )

        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)

        """ Find a Field Day with no Site attribute """
        fieldDay = filter(lambda x: 'sites' not in x, fieldDayTestData.fieldDayList)[0]
        fieldDayId = fieldDay["_id"]

        """ Get a site code which is valid for the Field Day location """
        location = filter(lambda x: x["_id"] == fieldDay["location_id"], [loc for loc in fieldDayTestData.locationList])[0]
        siteCode = location["sites"][0]["site_code"]

        response = self.fetch(
            "/field_days/{field_day_id}/sites".format(
                field_day_id=fieldDayId
            ),
            method="POST",
            body="site_code={siteCode}".format(siteCode=siteCode),
            follow_redirects=False
        )
        self.assertEqual(response.code, 201)


if __name__ == "__main__":
    tornado.testing.main()
