import unittest
from nose.tools import *
from persistence.SurveyListPersistenceBase import PersistentSurveyListDummy


class TestReefwatchSite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    def test_basic(self):
        dummySurveyListGetter = PersistentSurveyListDummy()
        dummySurveyList = dummySurveyListGetter.get(limit=10, offset=0, query="type='active'")
        self.assertIsInstance(dummySurveyList, list)
        print "I RAN!"
