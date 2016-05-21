from bson.objectid import ObjectId
import tornado.testing

from persistence.FieldDaySiteListMongo import PersistentFieldDaySiteList as FieldDaySiteList

import mongomock
import fieldDayTestData
mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)


class TestReefwatchFieldDay(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_list_get(self):
        """ Get a list of Sites for a given Field Day """

        """ Find a Field Day with at least one Site """
        fieldDayId = filter(lambda x: 'sites' in x and len(x['sites']) > 0, fieldDayTestData.fieldDayList)[0]["_id"]

        listGetter = FieldDaySiteList(mongoCollectionFieldDay)
        recordLimit = 10
        fieldDaySiteList, totalRecordCount = yield listGetter.get(
            fieldDayId=fieldDayId,
            limit=recordLimit,
            offset=0
        )
        self.assertIsInstance(fieldDaySiteList, list)
        self.assertEqual(
            len(fieldDaySiteList),
            totalRecordCount if totalRecordCount <= recordLimit else recordLimit
        )

    @tornado.testing.gen_test
    def test_empty_list_get(self):
        """ Get an empty list of Sites for a given Field Day """

        """ Find a Field Day with at least zero Sites """
        fieldDayId = filter(lambda x: 'sites' in x and len(x['sites']) == 0, fieldDayTestData.fieldDayList)[0]["_id"]

        listGetter = FieldDaySiteList(mongoCollectionFieldDay)
        recordLimit = 10
        fieldDaySiteList, totalRecordCount = yield listGetter.get(
            fieldDayId=fieldDayId,
            limit=recordLimit,
            offset=0
        )
        self.assertIsInstance(fieldDaySiteList, list)
        self.assertEqual(
            len(fieldDaySiteList),
            0
        )

    @tornado.testing.gen_test
    def test_nonexistent_list_get(self):
        """ Request a list of Sites for a given Field Day where there is no 'sites' attribute """

        """ Find a Field Day with no Site attribute """
        fieldDayId = filter(lambda x: 'sites' not in x, fieldDayTestData.fieldDayList)[0]["_id"]

        listGetter = FieldDaySiteList(mongoCollectionFieldDay)
        recordLimit = 10
        fieldDaySiteList, totalRecordCount = yield listGetter.get(
            fieldDayId=fieldDayId,
            limit=recordLimit,
            offset=0
        )
        self.assertIsNone(fieldDaySiteList)

