import unittest
from nose.tools import *
from persistence.SurveyListPersistenceBase import PersistentSurveyTypeListDummy


class TestReefwatchSite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    def test_basic(self):
        dummySurveyListGetter = PersistentSurveyTypeListDummy()
        dummySurveyList = dummySurveyListGetter.get(limit=10, offset=0, query="type='active'")
        self.assertIsInstance(dummySurveyList, list)
        print "I RAN!"
