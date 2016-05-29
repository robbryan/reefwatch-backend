from bson.objectid import ObjectId
import tornado.testing

from persistence.FieldDayMongo import PersistentFieldDayTides as FieldDayTides

import mongomock
import fieldDayTestData



class TestReefwatchFieldDayTides(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"
        cls.mongoCollectionFieldDay = mongomock.MongoClient().db.collection
        for obj in fieldDayTestData.fieldDayList:
            cls.mongoCollectionFieldDay.insert(obj)

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_collection_get(self):
        """ Get a collection of Tides for a given Field Day """

        """ Find a Field Day with a Tides collection with at least one tide """
        fieldDayId = filter(lambda x: 'tides' in x and any(x['tides']), fieldDayTestData.fieldDayList)[0]["_id"]

        getter = FieldDayTides(self.mongoCollectionFieldDay)
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

        getter = FieldDayTides(self.mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsInstance(fieldDayTides, dict)
        self.assertFalse(any(fieldDayTides))

    @tornado.testing.gen_test
    def test_nonexistent_colleciton_get(self):
        """ Request a collection of Tides for a given Field Day where there is no 'tides' attribute """

        """ Find a Field Day with no Site attribute """
        fieldDayId = filter(lambda x: 'tides' not in x, fieldDayTestData.fieldDayList)[0]["_id"]

        getter = FieldDayTides(self.mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsNone(fieldDayTides)

    @tornado.testing.gen_test
    def test_get_for_nonexistent_field_day(self):
        """ Request a collection of Tides for a given Field Day where there is no 'tides' attribute """

        """ Find a Field Day with no Site attribute """
        fieldDayId = '000000000000000000000000'

        getter = FieldDayTides(self.mongoCollectionFieldDay)
        fieldDayTides = yield getter.get(
            fieldDayId=fieldDayId
        )
        self.assertIsNone(fieldDayTides)


class TestReefwatchFieldDayTides_Updates(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"
        cls.mongoCollectionFieldDay = mongomock.MongoClient().db.collection
        for obj in fieldDayTestData.fieldDayList:
            cls.mongoCollectionFieldDay.insert(obj)

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_collection_update(self):
        """ Overwrite a collection of Tides for a given Field Day """

        """ Find a Field Day with a Tides collection with at least one tide """
        fieldDayId = filter(lambda x: 'tides' in x and any(x['tides']), fieldDayTestData.fieldDayList)[0]["_id"]

        setter = FieldDayTides(self.mongoCollectionFieldDay)
        updateCount = yield setter.update(
            fieldDayId=fieldDayId,
            tides={"high": {"time": "03:55:00", "height": 1.00}, "low": {"time": "09:22:00", "height": 0.50}}
        )
        self.assertEqual(1, updateCount)
        updatedTides = self.mongoCollectionFieldDay.find_one({"_id": fieldDayId}, {"tides": 1})["tides"]
        self.assertDictContainsSubset({"time": "03:55:00", "height": 1.00}, updatedTides["high"])
        self.assertDictContainsSubset({"time": "09:22:00", "height": 0.50}, updatedTides["low"])

    @tornado.testing.gen_test
    def test_empty_collection_update(self):
        """ Populate an empty collection of Tides for a given Field Day """

        """ Find a Field Day with a Tides attribute with no values """
        fieldDayId = filter(lambda x: "tides" in x and not any(x["tides"]), fieldDayTestData.fieldDayList)[0]["_id"]

        setter = FieldDayTides(self.mongoCollectionFieldDay)
        updateCount = yield setter.update(
            fieldDayId=fieldDayId,
            low={"time": "09:38:00", "height": 0.76}
        )
        self.assertEqual(1, updateCount)
        updatedTides = self.mongoCollectionFieldDay.find_one({"_id": fieldDayId}, {"tides": 1})["tides"]
        self.assertDictContainsSubset({"time": "09:38:00", "height": 0.76}, updatedTides["low"])

    @tornado.testing.gen_test
    def test_nonexistent_tides_update(self):
        """ populate a collection of Tides for a given Field Day where there is no 'tides' attribute """

        """ Find a Field Day with no Site attribute """
        fieldDayId = filter(lambda x: 'tides' not in x, fieldDayTestData.fieldDayList)[0]["_id"]

        """ Add a 'high' Tide for a given Field Day where there is no 'tides' attribute """

        setter = FieldDayTides(self.mongoCollectionFieldDay)
        updateCount = yield setter.update(
            fieldDayId=fieldDayId,
            high={"time": "02:50:00", "height": 0.81}
        )
        self.assertEqual(updateCount, 1)
        updatedTides = self.mongoCollectionFieldDay.find_one({"_id": fieldDayId}, {"tides": 1})["tides"]
        self.assertDictContainsSubset({"time": "02:50:00", "height": 0.81}, updatedTides["high"])


if __name__ == "__main__":
    pass
