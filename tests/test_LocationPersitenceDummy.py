import tornado.testing
from persistence.LocationPersistenceDummy import PersistentLocationDummy


class TestReefwatchSite(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_basic(self):
        """ Get a single location by ID """
        dummyEntityGetter = PersistentLocationDummy()
        dummyEntity = yield dummyEntityGetter.get(locationId="1000")
        self.assertIsInstance(dummyEntity, dict)
        self.assertTrue(any(dummyEntity))
        print "I RAN!"
