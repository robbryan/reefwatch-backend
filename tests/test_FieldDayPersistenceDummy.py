import unittest
import tornado.testing
from persistence.FieldDayPersistenceDummy import PersistentFieldDayDummy as EntityDummy


class TestReefwatchFieldDay(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_get_by_id(self):
        dummyEntityGetter = EntityDummy()
        dummyEntity = yield dummyEntityGetter.get(fieldDayId="90e49f7a-087b-11e6-ad28-902b34626bbb")
        self.assertIsInstance(dummyEntity, dict)
        self.assertTrue(any(dummyEntity))

