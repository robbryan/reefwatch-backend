import unittest
import tornado.httpserver 
import tornado.httpclient 
import tornado.ioloop 
import tornado.web
from tornado.httputil import HTTPHeaders


import datetime
import simplejson
import os
import logging

""" Surveys """
from persistence.SurveyListPersistenceBase import PersistentSurveyListDummy as PersistentSurveyList
from surveyHandler import SurveyListHandler

""" Locations """
from persistence.LocationListPersistenceBase import PersistentLocationListDummy as PersistentLocationList
from locationHandler import LocationListHandler

""" Sites """
from persistence.SiteListPersistenceBase import PersistentSiteListDummy as PersistentSiteList
from siteHandler import SiteListHandler


class TestListHandlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        listenPort = 8989
        cls.__base_address__ = "http://localhost:{0}/".format(listenPort)
        application = tornado.web.Application([
                (r'/location', LocationListHandler, dict(persistentLocationListObj=PersistentLocationList())),
                (r'/location/([0-9]+)/sites', SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
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


    def testLocationListGet(self):
        """ Test getting list of Locations """
        http_client = tornado.httpclient.AsyncHTTPClient()

        """ Test with no params """
        http_request = tornado.httpclient.HTTPRequest(
            self.__base_address__ + "location", method='GET')
        http_client.fetch(http_request, self.handle_request)
        tornado.ioloop.IOLoop.instance().start()
        self.assertEqual(self.response.code, 200)

        """ Test with valid params """
        request_body = "per_page={0}".format(
            tornado.escape.url_escape("3")
            )
        http_request = tornado.httpclient.HTTPRequest(
            self.__base_address__ + "location?" + request_body, method='GET')
        http_client.fetch(http_request, self.handle_request)
        tornado.ioloop.IOLoop.instance().start()
        self.assertEqual(self.response.code, 200)
        self.assertTrue("X-Total-Count" in self.response.headers)
        totalRecordCount = int(self.response.headers["X-Total-Count"])


    @unittest.skip("Skipping")
    def testSurveyListGet(self):
        resourcePath = "surveys"
        """ Test getting list of Locations """
        http_client = tornado.httpclient.AsyncHTTPClient()

        """ Test with no params """
        http_request = tornado.httpclient.HTTPRequest(
            self.__base_address__ + resourcePath, method='GET')
        http_client.fetch(http_request, self.handle_request)
        tornado.ioloop.IOLoop.instance().start()
        self.assertEqual(self.response.code, 200)
        self.assertTrue("X-Total-Count" in self.response.headers)
        totalRecordCount = int(self.response.headers["X-Total-Count"])


if __name__=="__main__":
    unittest.main()

