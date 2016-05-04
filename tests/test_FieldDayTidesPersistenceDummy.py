import unittest
import tornado.testing
from persistence.FieldDayPersistenceDummy import PersistentFieldDayTidesDummy as EntityDummy


class TestReefwatchFieldDayTides(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_get_tides_for_field_day(self):
        dummyEntityGetter = EntityDummy()
        dummyEntity = yield dummyEntityGetter.get(fieldDayId="1100")
        print dummyEntity
        self.assertIsInstance(dummyEntity, dict)
        self.assertTrue(any(dummyEntity))

    @tornado.testing.gen_test
    def test_set_tides_for_field_day(self):
        dummyEntitySetter = EntityDummy()
        tideCount = yield dummyEntitySetter.update(
            fieldDayId="1200",
            high={"height": 1.88, "time": "05:17"},
            low={"height": 0.81, "time": "17:05"}
        )
        print tideCount
        self.assertGreater(tideCount, 0)
