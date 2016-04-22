import unittest
from nose.tools import *
from persistence.FieldDayListPersistenceBase import PersistentFieldDayListDummy as ListDummy


class TestReefwatchFieldDay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    def test_basic(self):
        dummyListGetter = ListDummy()
        dummyList, totalRecordCount = dummyListGetter.get(limit=100, offset=0, query="type='active'")
        self.assertIsInstance(dummyList, list)
        print "I RAN!"
