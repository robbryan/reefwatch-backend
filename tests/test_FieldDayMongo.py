import unittest
import tornado.testing
from persistence.FieldDayMongo import PersistentFieldDay as FieldDayOperator

import mongomock


class TestReefwatchFieldDay(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"
        cls.__collection__ = mongomock.MongoClient().db.collection
        cls.__collection__.insert_one({"id": "FOR UPDATE", "date": "2016-01-25", "location_id": "3000"})
        cls.__collection__.insert_one({"id": "FOR DELETE", "date": "2016-02-17", "location_id": "4000", "tides": {}})

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_get_known_field_day(self):
        newFieldDay = {
            "date": "2016-03-12",
            "description": "New Test Field Day",
            "tides": {},
            "location_id": "Location ID"
        }
        result = self.__collection__.insert_one(newFieldDay)
        newId = str(result.inserted_id)
        fieldDayOperator = FieldDayOperator(self.__collection__)
        fieldDayEntity = yield fieldDayOperator.get(fieldDayId=newId)
        self.assertIsInstance(fieldDayEntity, dict)
        self.assertTrue(any(fieldDayEntity))

    @tornado.testing.gen_test
    def test_get_non_existent_field_day(self):
        fieldDayOperator = FieldDayOperator(self.__collection__)
        fieldDayEntity = yield fieldDayOperator.get(fieldDayId=0)
        self.assertIsNone(fieldDayEntity)

    @tornado.testing.gen_test
    def test_get_known_field_day(self):
        result = self.__collection__.find_one({"id": "FOR UPDATE"})
        fieldDayId = str(result["_id"])
        fieldDayOperator = FieldDayOperator(self.__collection__)
        updateCount = yield fieldDayOperator.update(fieldDayId=fieldDayId, description="This is the updated description")
        self.assertEqual(updateCount, 1)
