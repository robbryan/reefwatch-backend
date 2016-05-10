import unittest
import tornado.httpserver 
import tornado.httpclient 
import tornado.ioloop 
import tornado.web
from tornado.httputil import HTTPHeaders
import tornado.escape

import datetime
import os
import logging

import mongomock

""" Surveys """
from persistence.SurveyListPersistenceBase import PersistentSurveyListDummy as PersistentSurveyList
from surveyHandler import SurveyListHandler

""" Locations """
from persistence.LocationListPersistenceBase import PersistentLocationListDummy as PersistentLocationList
from persistence.LocationPersistenceDummy import PersistentLocationDummy as PersistentLocationEntity
from locationHandler import LocationListHandler

""" Sites """
from persistence.SiteListPersistenceBase import PersistentSiteListDummy as PersistentSiteList
from siteHandler import SiteListHandler

""" Field Days """
from persistence.FieldDayPersistenceDummy import PersistentFieldDayListDummy as PersistentFieldDayList
from fieldDayHandler import FieldDayListHandler
from persistence.FieldDayListMongo import PersistentFieldDayList as FieldDayListMongo
import fieldDayTestData
mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)
FieldDayListMongo = FieldDayListMongo(mongoCollectionFieldDay)


class TestListHandlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        listenPort = 8989
        cls.__base_address__ = "http://localhost:{0}/".format(listenPort)
        application = tornado.web.Application([
                (
                    r"/dummy/field_days",
                    FieldDayListHandler,
                    dict(
                        persistentEntityListObj=PersistentFieldDayList(),
                        persistentLocationEntityObj=PersistentLocationEntity()
                    )
                ),
                (
                    r"/mongo/field_days",
                    FieldDayListHandler,
                    dict(
                        persistentEntityListObj=FieldDayListMongo,
                        persistentLocationEntityObj=PersistentLocationEntity()
                    )
                ),
                (r'/dummy/locations', LocationListHandler, dict(persistentLocationListObj=PersistentLocationList())),
                (r'/dummy/locations/([0-9]+)/sites', SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
                ]
            )
        application.settings = dict(
            )

        cls.http_server = tornado.httpserver.HTTPServer(application) 
        cls.http_server.listen(listenPort)
        logging.basicConfig(format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
        application.logger = logging.getLogger('Test Event logger')
        application.logger.setLevel(logging.DEBUG)



    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def handle_request(self, response): 
        self.response = response 
        tornado.ioloop.IOLoop.instance().stop()


    def testAllListGets(self):
        """ Test getting list of Locations, Sites and Field Days """
        http_client = tornado.httpclient.AsyncHTTPClient()

        for resourcePath in ["dummy/locations", "dummy/locations/123/sites", "dummy/field_days", "mongo/field_days"]:

            """ Test with no params """
            http_request = tornado.httpclient.HTTPRequest(
                self.__base_address__ + resourcePath, method='GET')
            http_client.fetch(http_request, self.handle_request)
            tornado.ioloop.IOLoop.instance().start()
            self.assertEqual(self.response.code, 200)
            self.assertTrue("X-Total-Count" in self.response.headers)
            totalRecordCount = int(self.response.headers["X-Total-Count"])

            self.assertTrue("Per_page" in self.response.headers)
            perPage = int(self.response.headers["Per_page"])

            responseJson = tornado.escape.json_decode(self.response.body)
            self.assertEqual(len(responseJson["data"]), totalRecordCount if perPage > totalRecordCount else perPage)

            """ Test with valid params """
            request_body = "per_page={0}".format(
                tornado.escape.url_escape("3")
                )
            http_request = tornado.httpclient.HTTPRequest(
                self.__base_address__ + resourcePath + "?" + request_body, method='GET')
            http_client.fetch(http_request, self.handle_request)
            tornado.ioloop.IOLoop.instance().start()
            self.assertEqual(self.response.code, 200)


if __name__=="__main__":
    unittest.main()

