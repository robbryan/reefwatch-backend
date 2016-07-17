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
            query={"email": "christopher.robin@hundred.acre.wood"}
        )
        self.assertIsInstance(userList, list)
        self.assertEqual(len(userList), 1)
        user = userList.pop()
        self.assertEqual(user["user_handle"], "Billy Moon")

    @classmethod
    def getTestData(self):
        return [
            {
                "_id": ObjectId('57849bdf64cc932fc08858d3'),
                "user_handle": "Billy Moon",
                "full_name": "Christopher Robin",
                "email_addresses": [{"email": "christopher.robin@hundred.acre.wood", "status": "active", "create_date_time": "2016-05-03 09:38:17"}],
                "status": "active",
                "create_date_time": "2016-05-03 09:38:17"
            },
            {
                "_id": ObjectId('578aefe0c1ed600ab7ac764a'),
                "user_handle": "Test 1",
                "full_name": "Test User One",
                "email_addresses": [
                    {
                        "email": "testuser.1@company.com",
                        "status": "active",
                        "create_date_time": "2016-05-07 19:02:54"
                    },
                    {
                        "email": "one.testuser@acme.com",
                        "status": "inactive",
                        "create_date_time": "2016-06-14 11:11:23"
                    }
                ],
                "status": "active",
                "create_date_time": "2016-05-07 19:02:54"
            }
        ]
