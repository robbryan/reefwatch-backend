from bson.objectid import ObjectId
import tornado.testing

from persistence.UserListMongo import PersistentUserList as UserList

import mongomock


class TestReefwatchUserList(tornado.testing.AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        print "Setup"
        cls.__collection__ = mongomock.MongoClient().db.collection
        for obj in cls.getTestData():
            cls.__collection__.insert(obj)

    @classmethod
    def tearDownClass(cls):
        print "Teardown"

    @tornado.testing.gen_test
    def test_list_get(self):
        listGetter = UserList(self.__collection__)
        recordLimit = 10
        userList, totalRecordCount = yield listGetter.get(
            limit=recordLimit,
            offset=0,
            query={"survey_type": "PIT", "location_id": "1000"}
        )
        self.assertIsInstance(userList, list)
        self.assertEqual(len(userList), 1)

    @classmethod
    def getTestData(self):
        return [
            {
                "_id": ObjectId('57849bdf64cc932fc08858d3'),
                "handle": "Billy Moon",
                "full_name": "Christopher Robin",
                "email_addresses": [{"email": "christopher.robin@hundred.acre.wood", "status": "active", "create_date_time": "2016-05-03 09:38:17"}],
                "status": "active",
                "create_date_time": "2016-05-03 09:38:17"
            }
        ]
