import tornado.testing
import tornado.web
from tornado.httputil import HTTPHeaders
import tornado.escape

import logging

import mongomock

import fieldDayTestData

""" Surveys """
from persistence.SurveyTypeListMongo import PersistentSurveyTypeList as SurveyTypeList
from persistence.FieldDaySurveyListMongo import PersistentFieldDaySurveyList
from surveyHandler import SurveyTypeListHandler, FieldDaySurveyListHandler
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
from persistence.FieldDaySiteListMongo import PersistentFieldDaySiteList
from siteHandler import SiteListHandler
from fieldDaySiteHandler import FieldDaySiteListHandler

""" Field Days """
from fieldDayHandler import FieldDayListHandler
from persistence.FieldDayListMongo import PersistentFieldDayList as FieldDayListMongo
from persistence.FieldDayMongo import PersistentFieldDay as FieldDayMongo
mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)
FieldDayListMongo = FieldDayListMongo(mongoCollectionFieldDay)
FieldDayMongo = FieldDayMongo(mongoCollectionFieldDay)


class TestListHandlers(tornado.testing.AsyncHTTPTestCase):

    __cookieSecret__ = "THIS_IS_THE_TEST_COOKIE_SECRET"

    def __init__(self, *rest):
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    def get_app(self):
        application = tornado.web.Application([
                (
                    r"/mongo/field_days",
                    FieldDayListHandler,
                    dict(
                        persistentEntityListObj=FieldDayListMongo,
                        persistentLocationEntityObj=LocationListMongo
                    )
                ),
                (
                    r"/mongo/field_days/([A-Za-z0-9]+)/sites/(ANU)/surveys",
                    FieldDaySurveyListHandler,
                    dict(
                        persistentFieldDaySurveyListObj=PersistentFieldDaySurveyList(mongoCollectionFieldDay)
                    )
                ),
                (
                    r"/mongo/field_days/([A-Za-z0-9]+)/sites",
                    FieldDaySiteListHandler,
                    dict(
                        persistentFieldDaySiteListObj=PersistentFieldDaySiteList(mongoCollectionFieldDay),
                        persistentLocationEntityObj=LocationEntityMongo,
                        persistentFieldDayEntityObj=FieldDayMongo
                    )
                ),
                (r'/mongo/locations', LocationListHandler, dict(persistentLocationListObj=LocationListMongo)),
                (r'/mongo/surveys', SurveyTypeListHandler, dict(persistentSurveyListObj=SurveyTypeList(mongoCollectionSurveyType))),
#                (r'/mongo/locations/([A-Za-z0-9]+)/sites', SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__
            )

        return application

    def test_allListGets(self):
        """ Test getting list of Locations, Sites and Field Days """

        for resourcePath in [
            "/mongo/locations",
            "/mongo/surveys",
            "/mongo/field_days",
            "/mongo/field_days/573e765fc1ed602daf609007/sites",
            "/mongo/field_days/573e765fc1ed602daf609007/sites/ANU/surveys"
            ]:

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

            """ Test with invalid params """
            queryString = "per_page={0}".format(
                tornado.escape.url_escape("abc")
                )
            response = self.fetch(resourcePath + "?" + queryString, method='GET')
            self.assertEqual(response.code, 400)


if __name__=="__main__":
    tornado.testing.main()

