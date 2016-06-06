import tornado.testing
import tornado.web
import tornado.escape

from authHandlerDummy import DummyLoginHandler
from siteHandler import SiteListHandler
from persistence.LocationSiteListMongo import PersistentLocationSiteList as LocationSiteList

import logging
import Cookie
import mongomock
import fieldDayTestData


class TestLocationSiteListHandler_unauthenticated(tornado.testing.AsyncHTTPTestCase):

    __cookieSecret__ = "THIS_IS_THE_TEST_COOKIE_SECRET"

    def __init__(self, *rest):
        self.cookies = Cookie.SimpleCookie()
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    @classmethod
    def setUpClass(cls):
        cls.mongoCollectionLocationSite = mongomock.MongoClient().db.collection
        for obj in fieldDayTestData.locationList:
            cls.mongoCollectionLocationSite.insert(obj)

    @classmethod
    def tearDownClass(cls):
        pass

    def get_app(self):
        application = tornado.web.Application([
                (
                    r'/locations/([A-Za-z0-9]+)/sites',
                    SiteListHandler,
                    dict(persistentEntityListObj=LocationSiteList(self.mongoCollectionLocationSite))
                )
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_unauthenticatedGET(self):
        """ Test that it's possible to get Location Sites without authenticating """

        """ Find a Location with a Sites collection with at least one site """
        for locationId in [x["_id"] for x in fieldDayTestData.locationList]:
            response = self.fetch("/locations/{location_id}/sites".format(location_id=locationId), follow_redirects=False)
            self.assertEqual(response.code, 200)
            responseJson = tornado.escape.json_decode(response.body)
            self.assertTrue(any(responseJson))

    def test_unauthenticatedOPTIONS(self):
        """ Test that OPTIONS allowed when un-authenticated is only GET """

        """ Find a Location with a Sites collection with at least one site """
        locationId = filter(lambda x: 'sites' in x and any(x['sites']), fieldDayTestData.locationList)[0]["_id"]
        response = self.fetch("/locations/{location_id}/sites".format(location_id=locationId), method="OPTIONS", follow_redirects=False)
        self.assertEqual(response.code, 200)
        self.assertTrue("Access-Control-Allow-Methods" in response.headers)
        self.assertItemsEqual(["GET", "OPTIONS"], response.headers["Access-Control-Allow-Methods"].split(','))

    def test_unauthenticatedPOST(self):
        """ Test that POST is not allowed when un-authenticated """

        """ Find a Location """
        locationId = filter(lambda x: any(x), fieldDayTestData.locationList)[0]["_id"]
        response = self.fetch(
            "/locations/{location_id}/sites".format(
                location_id=locationId
            ),
            method="POST",
            body=tornado.escape.json_encode({}),
            follow_redirects=False
        )
        self.assertIn(response.code, [302, 403, 405])


if __name__ == "__main__":
    tornado.testing.main()
