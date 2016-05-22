from bson.objectid import ObjectId
import tornado.testing

from persistence.FieldDayMongo import PersistentFieldDayTides as FieldDayTides

import mongomock
import fieldDayTestData
mongoCollectionFieldDay = mongomock.MongoClient().db.collection
for obj in fieldDayTestData.fieldDayList:
    mongoCollectionFieldDay.insert(obj)


class TestReefwatchFieldDayTides(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_collection_get(self):
        """ Get a collection of Tides for a given Field Day """

        """ Find a Field Day with a Tides collection with at least one tide """
        fieldDayId = filter(lambda x: 'tides' in x and any(x['tides']), fieldDayTestData.fieldDayList)[0]["_id"]

        getter = FieldDayTides(mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsInstance(fieldDayTides, dict)
        self.assertIn("high", fieldDayTides)

    @tornado.testing.gen_test
    def test_empty_collection_get(self):
        """ Get an empty collection of Tides for a given Field Day """

        """ Find a Field Day with a Tides attribute with no values """
        fieldDayId = filter(lambda x: "tides" in x and not any(x["tides"]), fieldDayTestData.fieldDayList)[0]["_id"]

        getter = FieldDayTides(mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsInstance(fieldDayTides, dict)
        self.assertFalse(any(fieldDayTides))

    @tornado.testing.gen_test
    def test_nonexistent_collection_get(self):
        """ Request a collection of Tides for a given Field Day where there is no 'tides' attribute """

        """ Find a Field Day with no Site attribute """
        fieldDayId = filter(lambda x: 'tides' not in x, fieldDayTestData.fieldDayList)[0]["_id"]

        getter = FieldDayTides(mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsNone(fieldDayTides)

