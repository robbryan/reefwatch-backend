import unittest
import tornado.testing
from persistence.FieldDayPersistenceDummy import PersistentFieldDayListDummy as ListDummy


class TestReefwatchFieldDay(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_basic(self):
        dummyListGetter = ListDummy()
        dummyList, totalRecordCount = yield dummyListGetter.get(limit=100, offset=0, query="type='active'")
        self.assertIsInstance(dummyList, list)
        print "I RAN!"
