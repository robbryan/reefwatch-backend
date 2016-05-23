import tornado.testing

from persistence.SurveyTypeListMongo import PersistentSurveyTypeList as SurveyTypeList

import mongomock
import fieldDayTestData
mongoCollectionSurveyType = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.surveyTypeList:
    mongoCollectionSurveyType.insert(obj)


class TestReefwatchSurveyTypeList(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_list_get(self):
        """ Get a list of Survey Types """

        listGetter = SurveyTypeList(mongoCollectionSurveyType)
        recordLimit = 10
        fieldDaySiteList, totalRecordCount = yield listGetter.get(
            limit=recordLimit,
            offset=0
        )
        self.assertIsInstance(fieldDaySiteList, list)
        self.assertEqual(
            len(fieldDaySiteList),
            totalRecordCount if totalRecordCount <= recordLimit else recordLimit
        )
