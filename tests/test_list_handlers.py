import tornado.testing
import tornado.web
from tornado.httputil import HTTPHeaders
import tornado.escape

import logging

import mongomock

import fieldDayTestData

""" Surveys """
from persistence.SurveyTypeListMongo import PersistentSurveyTypeList as SurveyTypeList
from surveyHandler import SurveyTypeListHandler
mongoCollectionSurveyType = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.surveyTypeList:
    mongoCollectionSurveyType.insert(obj)


""" Locations """
from persistence.LocationMongo import PersistentLocation as LocationEntityMongo
from persistence.LocationListMongo import PersistentLocationList as LocationListMongo
from locationHandler import LocationListHandler
mongoCollectionLocation = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.locationList:
    mongoCollectionLocation.insert(obj)
LocationListMongo = LocationListMongo(mongoCollectionLocation)
LocationEntityMongo = LocationEntityMongo(mongoCollectionLocation)

""" Sites """
from persistence.SiteListPersistenceBase import PersistentSiteListDummy as PersistentSiteList
from siteHandler import SiteListHandler

""" Field Days """
from persistence.FieldDayPersistenceDummy import PersistentFieldDayListDummy as PersistentFieldDayList
from fieldDayHandler import FieldDayListHandler
from persistence.FieldDayListMongo import PersistentFieldDayList as FieldDayListMongo
mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)
FieldDayListMongo = FieldDayListMongo(mongoCollectionFieldDay)


class TestListHandlers(tornado.testing.AsyncHTTPTestCase):

    def __init__(self, *rest):
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    def get_app(self):
        application = tornado.web.Application([
                (
                    r"/dummy/field_days",
                    FieldDayListHandler,
                    dict(
                        persistentEntityListObj=PersistentFieldDayList(),
                        persistentLocationEntityObj=LocationListMongo
                    )
                ),
                (
                    r"/mongo/field_days",
                    FieldDayListHandler,
                    dict(
                        persistentEntityListObj=FieldDayListMongo,
                        persistentLocationEntityObj=LocationEntityMongo
                    )
                ),
                (r'/dummy/locations', LocationListHandler, dict(persistentLocationListObj=LocationListMongo)),
                (r'/dummy/locations/([0-9]+)/sites', SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
                ]
            )
        application.settings = dict(
            )

        return application

    def test_allListGets(self):
        """ Test getting list of Locations, Sites and Field Days """

        for resourcePath in ["/dummy/locations", "/dummy/locations/123/sites", "/dummy/field_days", "/mongo/field_days"]:

            """ Test with no params """
            response = self.fetch(resourcePath)
            self.assertEqual(response.code, 200)
            self.assertTrue("X-Total-Count" in response.headers)
            totalRecordCount = int(response.headers["X-Total-Count"])

            print "{0}: {1}".format(resourcePath, totalRecordCount)

            self.assertTrue("Per_page" in response.headers)
            perPage = int(response.headers["Per_page"])

            responseJson = tornado.escape.json_decode(response.body)
            self.assertEqual(len(responseJson["data"]), totalRecordCount if perPage > totalRecordCount else perPage)

            """ Test with valid params """
            queryString = "per_page={0}".format(
                tornado.escape.url_escape("3")
                )
            response = self.fetch(resourcePath + "?" + queryString, method='GET')
            self.assertEqual(response.code, 200)


if __name__=="__main__":
    tornado.testing.main()

