import unittest
from nose.tools import *
from persistence.FieldDayListPersistenceBase import PersistentFieldDayListDummy as ListDummy

from tornado.gen import coroutine

class TestReefwatchFieldDay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @coroutine
    def test_basic(self):
        dummyListGetter = ListDummy()
        dummyList, totalRecordCount = yield dummyListGetter.get(limit=100, offset=0, query="type='active'")
        self.assertIsInstance(dummyList, list)
        print "I RAN!"
