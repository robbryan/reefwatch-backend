import unittest
import tornado.testing
from persistence.FieldDayMongo import PersistentFieldDay as FieldDayOperator

import mongomock


class TestReefwatchFieldDay(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"
        cls.__collection__ = mongomock.MongoClient().db.collection

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
