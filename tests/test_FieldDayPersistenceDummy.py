import unittest
from nose.tools import *
from persistence.FieldDayPersistenceBase import PersistentFieldDayDummy as EntityDummy

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
        dummyEntityGetter = EntityDummy()
        dummyEntity = yield dummyEntityGetter.get(id="90e49f7a-087b-11e6-ad28-902b34626bbb")
        self.assertIsInstance(dummyEntity, dict)
        print "I RAN!"
